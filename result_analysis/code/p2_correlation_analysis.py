import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import statsmodels.api as sm

from settings import *
from utils import *


# p2.1 Is Defective
def is_defective_validate(combined_df):
    # correlation matrix
    # pearson
    corr_matrix_heatmap(combined_df, 'pearson', 'Is Defective (Pearson)')
    # spearman
    corr_matrix_heatmap(combined_df, 'spearman', 'Is Defective (Spearman)')
    # kendall
    corr_matrix_heatmap(combined_df, 'kendall', 'Is Defective (Kendall)')
    
    # line graph
    xy_plot(combined_df, 'Ownership', 'Is Defective') # Ownership vs Is Defective
    xy_plot(combined_df, 'Num of Minor 10%', 'Is Defective') # Number of Minor vs Is Defective
    xy_plot(combined_df, 'Per of Minor 10%', 'Is Defective') # Per of Minor vs Is Defective
    xy_plot(combined_df, 'Days Difference', 'Is Defective') # Repo existing time vs Is Defective
    xy_plot(combined_df, 'Age', 'Is Defective') # Component age vs Is Defective
    xy_plot(combined_df, 'Oss Stage Aged Numeric', 'Is Defective') # Six Oss stage vs Is Defective
    
    # robust check (multiple linear regression)
    multi_linear_regression(['Days Difference'], 'Is Defective', combined_df) # Repo existing time
    multi_linear_regression(['Age'], 'Is Defective', combined_df) # Component age
    multi_linear_regression(['Days Difference', 'Code churn', 'File Size'], 'Is Defective', combined_df) # With Classic
    multi_linear_regression(['Age', 'Code churn', 'File Size'], 'Is Defective', combined_df)
    
    return


# p2.2 Vulnerable with AGE/TIME


# p2.3 CVE Severity


if __name__ == "__main__":
    # read csv
    cve_df = pd.read_csv(SETTINGS['cve results'])
    vulnerable_df = pd.read_csv(SETTINGS['vulnerable results'])
    non_vulnerable_df = pd.read_csv(SETTINGS['non vulnerable results'])

    # format df
    cve_df = format_df(cve_df, True)
    vulnerable_df = format_df(vulnerable_df, True)
    non_vulnerable_df = format_df(non_vulnerable_df, True)

    # combine df
    combined_df = combine_df(vulnerable_df, non_vulnerable_df)


    # p2.1
    is_defective_validate(combined_df)

    # p2.2


    # p2.3

