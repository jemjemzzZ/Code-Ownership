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


# p2.2 Vulnerable with AGE/TIME


# p2.3 CVE Severity



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



# Is Defective
# descriptive_statistics(combined_df)
# corr_matrix_heatmap(combined_df, 'pearson') # pearson
# corr_matrix_heatmap(combined_df, 'spearman') # spearman
# multi_linear_regression(['Per of Minor 10%'], 'Is Defective', combined_df)


# Vulnerable With Time/Age
corr_matrix_heatmap(vulnerable_df, 'pearson') # pearson
# corr_matrix_heatmap(pytorch_tensorflow_df, 'spearman') # spearman
# multi_linear_regression(['Churn rate'], 'Time Stage Aged Numeric', pytorch_tensorflow_df)


# Vulnerable With CVE Severity
# corr_matrix_heatmap(cve_df, 'pearson') # pearson
# corr_matrix_heatmap(cve_df, 'spearman') # spearman


# Group component performance
# group_vulnerable_df = group_component_df(pytorch_tensorflow_df)
# group_cve_df = group_component_df(cve_df)
# corr_matrix_heatmap(group_vulnerable_df, 'pearson') # pearson
# corr_matrix_heatmap(group_cve_df, 'spearman') # spearman