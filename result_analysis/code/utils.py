import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import statsmodels.api as sm


# descriptive statistics
def descriptive_statistics(df):
    print("##########Ownership##########")
    print(df['Ownership'].describe())
    print("##########Num of Contributor##########")
    print(df['Num of Contributor'].describe())
    print("##########Num of Minor 20%##########")
    print(df['Num of Minor 20%'].describe())
    print("##########Per of Minor 20%##########")
    print(df['Per of Minor 20%'].describe())
    print("##########Days Difference##########")
    print(df['Days Difference'].describe())
    print("##########Age##########")
    print(df['Age'].describe())
    print("##########Code churn##########")
    print(df['Code churn'].describe())
    print("##########Churn rate##########")
    print(df['Churn rate'].describe())
    print("##########File Size##########")
    print(df['File Size'].describe())
    print("##########Time Stage Numeric##########")
    print(df['Time Stage Numeric'].describe())
    print("##########Time Stage Aged Numeric##########")
    print(df['Time Stage Aged Numeric'].describe())
    print("##########Oss Stage Numeric##########")
    print(df['Oss Stage Numeric'].describe())
    print("##########Oss Stage Aged Numeric##########")
    print(df['Oss Stage Aged Numeric'].describe())


# correlation heatmap
def corr_matrix_heatmap(df, method_name):
    corr_matrix = df.corr(method=method_name)

    plt.figure(figsize=(15,15))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.subplots_adjust(bottom=0.3)
    plt.show()


# pearson correlation between attrs to attr
def attr_and_one_attribute(df, dependent, predictors):
    for predictor in predictors:
        corr, _ = pearsonr(df[predictor], df[dependent])
        print(f'Correlation between {predictor} and {dependent} is: {corr}')
        # Plotting
        plt.plot(df[predictor], df[dependent], '-o', color='blue')  # '-o' means line with dots at data points
        plt.xlabel(predictor)
        plt.ylabel(dependent)
        plt.grid(True)  # adds grid for better readability
        plt.show()


# multiple linear regression
def multi_linear_regression(predictors, dependent, df):
    X = df[predictors]
    X = sm.add_constant(X)
    y = df[dependent]

    model = sm.OLS(y, X).fit()
    print(model.summary())
    return


# format df
def format_df(df, is_non_numeric):
    # file size
    df['File Size'] =  df['File Size'].fillna(0)
    
    # time stage
    time_stage_mapping = {'t1': 1, 't2': 2, 't3':3, 't4':4, 't5': 5}
    df['Time Stage Numeric'] = df['Time Stage'].map(time_stage_mapping)
    df['Time Stage Aged Numeric'] = df['Time Stage Aged'].map(time_stage_mapping)
    df = df.dropna(subset=['Time Stage Aged'])
    
    # oss stage
    oss_stage_mapping = {'SI': 1, "TI": 2, "II":3, "IG": 4, "SG": 5, "TG": 6}
    df['Oss Stage Numeric'] = df['Oss Stage'].map(oss_stage_mapping)
    df['Oss Stage Aged Numeric'] = df['Oss Stage Aged'].map(oss_stage_mapping)
    
    # churn rate
    df['Code churn'] = df['Total Added'] + df['Total Deleted']
    df['Churn rate'] = np.where(df['File Size'] != 0, (df['Code churn'] / df['File Size']) * 100, 0)
    
    # exclude non-numeric
    if is_non_numeric:
        df = df.select_dtypes(include=['number', 'bool'])
    
    return df


# combine df
def combine_df(df1, df2):
    common_columns = df1.columns.intersection(df2.columns)
    df1 = df1[common_columns]
    df2 = df2[common_columns]
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df


# group component df
def group_component_df(df):
    rows = []
    for url, group_data in df.groupby('URL'):
        row = {'URL': url, 'Component Type': 'group', 'Is Defective': True}
        for col in group_data.select_dtypes(include=[np.number]).columns:
            row[col] = group_data[col].mean()    
        rows.append(row)
    
    df_new = pd.DataFrame(rows)
    
    # df = df.append(df_new, ignore_index=True)
    # # component type
    # component_mapping = {'file': 1, 'group': 2}
    # df['Component Type Numeric'] = df['Component Type'].map(component_mapping)
    
    return df_new









