import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import ks_2samp
from scipy.spatial.distance import pdist, squareform
import statsmodels.api as sm
from skbio import DistanceMatrix
from skbio.stats.distance import mantel
from sklearn.metrics.pairwise import cosine_similarity

from settings import *
from utils import *


# p2.1 proportion influence on dataset correlation performance
def proportion_validate(vulnerable_df, non_vulnerable_df):
    # generate different correlation matrix under proportions
    proportions = [(0.1, 1), (0.2, 1), (0.3, 1), (0.4, 1), (0.5, 1), 
                   (0.6, 1), (0.7, 1), (0.8, 1), (0.9, 1), (1.0, 1)]
    # proportions = [(0.01, 1), (0.05, 1), (0.1, 1), (0.5, 1), (1.0, 1)]
    matrix_list = []
    for prop in proportions:
        sample_df1 = vulnerable_df.sample(int(10000*prop[0]))
        sample_df2 = non_vulnerable_df.sample(int(10000*prop[1]))
        sample_combined_df = combine_df(sample_df1, sample_df2)
        matrix = sample_combined_df.corr()
        np.fill_diagonal(matrix.values, 0)
        matrix_list.append(matrix)
    
    # frobenius norm of matrix differences
    pairwise_frobenius_differences = []
    for i in range(len(matrix_list)):
        for j in range(i+1, len(matrix_list)):
            diff = np.linalg.norm(matrix_list[i] - matrix_list[j], 'fro')
            pairwise_frobenius_differences.append(diff)
    print("##########Frobenius Norm##########")
    print(pairwise_frobenius_differences)
    
    # similarity score
    min_val = min(pairwise_frobenius_differences)
    max_val = max(pairwise_frobenius_differences)
    similarity_scores = [1 - (val - min_val) / (max_val - min_val) for val in pairwise_frobenius_differences]
    similarity_scores_exp = [np.exp(-val) for val in pairwise_frobenius_differences]
    # Set up a subplot grid that has height 1 and width 2
    fig, axes = plt.subplots(1, 2, figsize=(18, 5))  # Adjust figsize as needed
    # Histogram
    axes[0].hist(similarity_scores, bins=50, edgecolor='k')
    axes[0].set_title(f"Min-Max Scaling Avg Score: {sum(similarity_scores)/len(similarity_scores)}")
    axes[0].set_xlabel('frobenius norm')
    axes[0].set_ylabel('Frequency')
    axes[1].hist(similarity_scores_exp, bins=50, edgecolor='k')
    axes[1].set_title(f"Exponential Decay Avg Score: {sum(similarity_scores_exp)/len(similarity_scores_exp)}")
    axes[1].set_xlabel('frobenius norm')
    axes[1].set_ylabel('Frequency')
    # Adjust layout
    plt.suptitle(f"Similarity Score")
    plt.tight_layout()
    plt.show()
    
    # mantel test
    mantel_results = []
    for i in range(len(matrix_list)):
        for j in range(i+1, len(matrix_list)):
            dm1 = DistanceMatrix(matrix_list[i])
            dm2 = DistanceMatrix(matrix_list[j])
            correlation, p_value, n = mantel(dm1, dm2, method='spearman', permutations=999)
            mantel_results.append((correlation, p_value))
    print("##########Mantel Test##########")
    for mantel_result in mantel_results:
        print(f"Correlation: {mantel_result[0]}, P-value: {mantel_result[1]}")
    
    return


# p2.2 threshold of minor influence on AGE/IS_DEFECTIVE correlation performance
def threshold_validate(combined_df, vulnerable_df, cve_df):
    # is defective
    print('##########Threshold vs Is_Defective##########')
    matrix_combined = combined_df.corr()
    matrix_combined_5 = matrix_combined.iloc[2:5, :]
    matrix_combined_10 = matrix_combined.iloc[5:8, :]
    matrix_combined_20 = matrix_combined.iloc[8:11, :]
    matrix_combined_50 = matrix_combined.iloc[11:14, :]
    matrix_combined_list = [matrix_combined_5, matrix_combined_10, matrix_combined_20, matrix_combined_50]
    
    # flatten matrix
    for i in range(0, len(matrix_combined_list)):
        for j in range(i+1, len(matrix_combined_list)):
            vector1 = matrix_combined_list[i].values.ravel()
            vector2 = matrix_combined_list[j].values.ravel()
            print(f'Threshold {i} vs Threshold {j}')
            # Cosine Similarity
            similarity = cosine_similarity([vector1], [vector2])
            print(f'Cosine Similarity: {similarity[0][0]}')
            # k-s test
            statistic, p_value = ks_2samp(vector1, vector2)
            print(f"K-S Statistic: {statistic} \t P-Value: {p_value}")
    
    # Vulnerable Time/Age
    print('##########Threshold vs Vulnerable##########')
    vulnerable_df = vulnerable_df.drop('Is Defective', axis=1).fillna(0)
    matrix_vulnerable = vulnerable_df.corr()
    matrix_vulnerable_5 = matrix_vulnerable.iloc[3:6, :]
    matrix_vulnerable_10 = matrix_vulnerable.iloc[6:9, :]
    matrix_vulnerable_20 = matrix_vulnerable.iloc[9:12, :]
    matrix_vulnerable_50 = matrix_vulnerable.iloc[12:15, :]
    matrix_vulnerable_list = [matrix_vulnerable_5, matrix_vulnerable_10, matrix_vulnerable_20, matrix_vulnerable_50]
    
    # flatten matrix
    for i in range(0, len(matrix_vulnerable_list)):
        for j in range(i+1, len(matrix_vulnerable_list)):
            vector1 = matrix_vulnerable_list[i].values.ravel()
            vector2 = matrix_vulnerable_list[j].values.ravel()
            print(f'Threshold {i} vs Threshold {j}')
            # Cosine Similarity
            similarity = cosine_similarity([vector1], [vector2])
            print(f'Cosine Similarity: {similarity[0][0]}')
            # k-s test
            statistic, p_value = ks_2samp(vector1, vector2)
            print(f"K-S Statistic: {statistic} \t P-Value: {p_value}")
    
    # CVE Severity
    print('##########Threshold vs CVE Severity##########')
    cve_df = cve_df.drop('Is Defective', axis=1).fillna(0)
    matrix_cve = cve_df.corr()
    matrix_cve_5 = matrix_cve.iloc[3:6, :]
    matrix_cve_10 = matrix_cve.iloc[6:9, :]
    matrix_cve_20 = matrix_cve.iloc[9:12, :]
    matrix_cve_50 = matrix_cve.iloc[12:15, :]
    matrix_cve_list = [matrix_cve_5, matrix_cve_10, matrix_cve_20, matrix_cve_50]
    
    # flatten matrix
    for i in range(0, len(matrix_cve_list)):
        for j in range(i+1, len(matrix_cve_list)):
            vector1 = matrix_cve_list[i].values.ravel()
            vector2 = matrix_cve_list[j].values.ravel()
            print(f'Threshold {i} vs Threshold {j}')
            # Cosine Similarity
            similarity = cosine_similarity([vector1], [vector2])
            print(f'Cosine Similarity: {similarity[0][0]}')
            # k-s test
            statistic, p_value = ks_2samp(vector1, vector2)
            print(f"K-S Statistic: {statistic} \t P-Value: {p_value}")
    
    return


# p2.3 group component influence on dataset correlation performance
def locality_validate(df):
    # group component df
    df = format_df(df, False)
    group_df = group_component_df(df)
    df_formatted = df.select_dtypes(include=['number', 'bool'])
    group_df_formatted = group_df.select_dtypes(include=['number', 'bool'])
    
    # format
    df_formatted = df_formatted.drop('Is Defective', axis=1).fillna(0)
    group_df_formatted = group_df_formatted.drop('Is Defective', axis=1).fillna(0)
    
    # matrix
    matrix1 = df_formatted.corr()
    np.fill_diagonal(matrix1.values, 0)
    matrix2 = group_df_formatted.corr()
    np.fill_diagonal(matrix2.values, 0)
    
    # mantel test
    dm1 = DistanceMatrix(matrix1)
    dm2 = DistanceMatrix(matrix2)
    correlation, p_value, n = mantel(dm1, dm2, method='spearman', permutations=999)
    print(f"Correlation: {correlation}, P-value: {p_value}")
    
    return


if __name__ == "__main__":
    # read csv
    cve_df = pd.read_csv(SETTINGS['cve results'])
    vulnerable_df = pd.read_csv(SETTINGS['vulnerable results'])
    non_vulnerable_df = pd.read_csv(SETTINGS['non vulnerable results'])

    # format df
    cve_df_formatted = format_df(cve_df, True)
    vulnerable_df_formatted = format_df(vulnerable_df, True)
    non_vulnerable_df_formatted = format_df(non_vulnerable_df, True)

    # combine df
    combined_df = combine_df(vulnerable_df_formatted, non_vulnerable_df_formatted)


    # p2.1
    # proportion_validate(vulnerable_df_formatted, non_vulnerable_df_formatted)

    # p2.2
    # threshold_validate(combined_df, vulnerable_df_formatted, cve_df_formatted)

    # p2.3
    # locality_validate(vulnerable_df)