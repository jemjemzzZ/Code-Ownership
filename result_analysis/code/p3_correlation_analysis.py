import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import statsmodels.api as sm

from settings import *
from utils import *


SAVE_FOLDER = SETTINGS['img folder'] + 'p3/'


# p3.1 Is Defective
def is_defective_validate(combined_df):
    # correlation matrix
    # pearson
    corr_matrix_heatmap(combined_df, 'pearson', 'Is Defective (Pearson)', SAVE_FOLDER)
    # spearman
    corr_matrix_heatmap(combined_df, 'spearman', 'Is Defective (Spearman)', SAVE_FOLDER)
    # kendall
    corr_matrix_heatmap(combined_df, 'kendall', 'Is Defective (Kendall)', SAVE_FOLDER)
    
    # robust check (multiple linear regression)
    multi_linear_regression(['Days Difference'], 'Is Defective', combined_df) # Repo existing time
    multi_linear_regression(['Days Difference', 'Code churn', 'File Size'], 'Is Defective', combined_df) # With Classic
    multi_linear_regression(['Age'], 'Is Defective', combined_df) # Component age
    multi_linear_regression(['Age', 'Code churn', 'File Size'], 'Is Defective', combined_df)
    
    return


# p3.2 Vulnerable with AGE/TIME
def metric_age(vulnerable_df):
    # correlation matrix
    # pearson
    corr_matrix_heatmap(vulnerable_df, 'pearson', 'Metric vs Time (Pearson)', SAVE_FOLDER)
    # spearman
    corr_matrix_heatmap(vulnerable_df, 'spearman', 'Metric vs Time (Spearman)', SAVE_FOLDER)
    # kendall
    corr_matrix_heatmap(vulnerable_df, 'kendall', 'Metric vs Time (Kendall)', SAVE_FOLDER)
    
    # robust check (multiple linear regression)
    multi_linear_regression(['Num of Minor 10%'], 'Time Stage Aged Numeric', vulnerable_df) # Minor
    multi_linear_regression(['Per of Minor 10%'], 'Time Stage Aged Numeric', vulnerable_df)
    multi_linear_regression(['Per of Minor 10%', 'Code churn', 'File Size'], 'Time Stage Aged Numeric', vulnerable_df) # controlled by classic
    multi_linear_regression(['Oss Stage Aged Numeric'], 'Time Stage Aged Numeric', vulnerable_df) # oss stage
    multi_linear_regression(['Oss Stage Aged Numeric', 'Code churn', 'File Size'], 'Time Stage Aged Numeric', vulnerable_df) # controlled by classic
    multi_linear_regression(['Per of Minor 10%', 'Oss Stage Aged Numeric'], 'Time Stage Aged Numeric', vulnerable_df) # minor + oss stage
    return


# p3.3 CVE Severity
def metric_cve(cve_df):
    # correlation matrix
    # pearson
    corr_matrix_heatmap(cve_df, 'pearson', 'Metric vs CVE Severity (Pearson)', SAVE_FOLDER)
    # spearman
    corr_matrix_heatmap(cve_df, 'spearman', 'Metric vs CVE Severity (Spearman)', SAVE_FOLDER)
    # kendall
    corr_matrix_heatmap(cve_df, 'kendall', 'Metric vs CVE Severity (Kendall)', SAVE_FOLDER)
    
    # robust check (multiple linear regression)
    multi_linear_regression(['Days Difference'], 'CVE Severity', cve_df) # Days difference
    multi_linear_regression(['Days Difference', 'Code churn', 'File Size'], 'CVE Severity', cve_df) # controlled by classic
    multi_linear_regression(['Age'], 'CVE Severity', cve_df) # Age
    multi_linear_regression(['Days Difference', 'Per of Minor 10%'], 'CVE Severity', cve_df) # controlled by minor
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
    is_defective_validate(combined_df)

    # p2.2
    metric_age(vulnerable_df_formatted)

    # p2.3
    metric_cve(cve_df_formatted)

