import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.api as sm


def corr_matrix_heatmap(df):
    corr_matrix = df.corr()

    plt.figure(figsize=(15,15))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()
    
    
def attr_and_one_attribute(df, attr, attrs):
    for attribute in attributes:
        corr, _ = pearsonr(df[attr], df[attribute])
        print(f'Correlation between {attr} and {attribute} is: {corr}')


def attr_and_multi_attributes(df):
    X = df[["Ownership", "Num of Minor 5%", "Days Difference"]] # Add more attributes if needed
    X = sm.add_constant(X) # Adds a constant term to the predictor
    y = df["CVE Severity"]

    model = sm.OLS(y, X).fit()
    print(model.summary())


# df = pd.read_csv("results.csv")
# df['File Size'] = df['File Size'].fillna(0)
# corr_matrix_heatmap(df)

# Read the CSV files into DataFrames
df1 = pd.read_csv('cve_results.csv')
df2 = pd.read_csv('non_vulnerable_results.csv')

common_columns = df1.columns.intersection(df2.columns)
df1 = df1[common_columns]
df2 = df2[common_columns]

# Concatenate the two DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df['File Size'] = combined_df['File Size'].fillna(0)
corr_matrix_heatmap(combined_df)

