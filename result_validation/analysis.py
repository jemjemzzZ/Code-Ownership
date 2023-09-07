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
    
    
def severity_and_one_attribute(df):
    attributes = ["Ownership", "Num of Minor 5%", "Num of Minor 10%", "Num of Minor 20%", "Num of Minor 50%", 
                  "Days Difference", "Age", "Total Added", "Total Deleted", "File Size"] # and other columns
    for attr in attributes:
        corr, _ = pearsonr(df['CVE Severity'], df[attr])
        print(f'Correlation between vulnerability_score and {attr} is: {corr}')


def severity_and_multi_attributes(df):
    X = df[["Ownership", "Num of Minor 5%", "Days Difference"]] # Add more attributes if needed
    X = sm.add_constant(X) # Adds a constant term to the predictor
    y = df["CVE Severity"]

    model = sm.OLS(y, X).fit()
    print(model.summary())


df = pd.read_csv("results.csv")
df['File Size'] = df['File Size'].fillna(0)
# corr_matrix_heatmap(df)
severity_and_one_attribute(df)
# severity_and_multi_attributes(df)
