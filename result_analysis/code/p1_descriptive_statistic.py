import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

from settings import *
from utils import *


SAVE_FOLDER = SETTINGS['img folder'] + 'p1/'


# p1.1 Descriptive statistics
def descriptive_statistics(df, columns):
    for column in columns:
        df_new = df.dropna(subset=[column])
        column_data = df_new[column]
        
        descriptive_statistics = column_data.describe()
        std_error = column_data.std() / (len(column_data)**0.5)
        
        print(f"#####Descriptive Statistic {column}#####")
        print(descriptive_statistics)
        print(f"Std. Error: {std_error}")
        print()


# p1.2 Histogram, box plot, normal Q-Q plot
def diagrams(df, columns):
    for column in columns:
        df_new = df.dropna(subset=[column])
        column_data = df_new[column]
        
        # Set up a subplot grid that has height 1 and width 3
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # Adjust figsize as needed

        # Histogram
        axes[0].hist(column_data, bins=50, edgecolor='k')
        axes[0].set_title('Histogram')
        axes[0].set_xlabel('Amounts')
        axes[0].set_ylabel('Frequency')

        # Boxplot
        axes[1].boxplot(column_data)
        axes[1].set_title('Boxplot')

        # Q-Q plot
        stats.probplot(column_data, plot=axes[2])
        axes[2].set_title('Q-Q plot')

        # Adjust layout
        plt.suptitle(f"Diagrams {column}")
        plt.tight_layout()
        
        # save
        save_path = f"{SAVE_FOLDER}diagrams_{column}.png"
        fig.savefig(save_path)
        
        # plt.show()


# p1.3 Skewness and Kurtosis check
def skewness_kurtosis(df, columns):
    for column in columns:
        df_new = df.dropna(subset=[column])
        column_data = df_new[column]
        
        skewness = stats.skew(column_data)
        kurtosis = stats.kurtosis(column_data)

        # Assuming an approximate standard error for skewness and kurtosis (SE = sqrt(6/N) for Skewness, SE = sqrt(24/N) for Kurtosis, N = sample size)
        std_error_skew = (6/len(column_data))**0.5
        std_error_kurt = (24/len(column_data))**0.5

        z_value_skew = skewness / std_error_skew
        z_value_kurt = kurtosis / std_error_kurt

        print(f"Skewness and Kurtosis {column}")
        print(f"Skewness: {skewness:.4f}, Standard Error: {std_error_skew:.4f}, Z-value: {z_value_skew:.4f}")
        print(f"Kurtosis: {kurtosis:.4f}, Standard Error: {std_error_kurt:.4f}, Z-value: {z_value_kurt:.4f}")
        print()


# p1.4 Shaprio-Wilk and Kologorow-Smirnow tests
def sw_ks_tests(df, columns):
    for column in columns:
        df_new = df.dropna(subset=[column])
        column_data = df_new[column]
        
        print(f"S-W and K-S tests {column}")
        
        # Shapiro-Wilk Test
        shapiro_stat, shapiro_sig = stats.shapiro(column_data)
        print(f"Shapiro-Wilk Test: Statistic = {shapiro_stat:.4f}, Sig. = {shapiro_sig:.4f}")

        # Kolmogorov-Smirnov Test (against a normal distribution)
        ks_stat, ks_sig = stats.kstest(column_data, 'norm')
        print(f"Kolmogorov-Smirnov Test: Statistic = {ks_stat:.4f}, Sig. = {ks_sig:.4f}")
        
        print()


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
    
    # columns
    columns = ['CVE Severity', 'Ownership', 
               'Num of Minor 10%', 'Per of Minor 10%', 'Avg of Minor Contri 10%', 
               'Days Difference', 'Age', 'Time Stage Aged Numeric', 'Oss Stage Aged Numeric', 
               'File Size', 'Code churn', 'Churn rate']
    
    # p1.1
    descriptive_statistics(vulnerable_df_formatted, columns)
    
    # p1.2
    diagrams(vulnerable_df_formatted, columns)
    
    # p1.3
    skewness_kurtosis(vulnerable_df_formatted, columns)
    
    # p1.4
    sw_ks_tests(vulnerable_df_formatted, columns)