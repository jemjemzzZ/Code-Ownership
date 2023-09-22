import pandas as pd
import os

def join_csvs(directory, output_file):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Read and concatenate all the CSV files
    df_list = [pd.read_csv(os.path.join(directory, file)) for file in files]
    concatenated_df = pd.concat(df_list, ignore_index=True)

    # Save the concatenated dataframe to a new CSV file
    concatenated_df.to_excel(output_file, index=False)
    print(f"All CSVs combined and saved to {output_file}")

if __name__ == "__main__":
    directory_path = "./distilled/"
    output_file_path = "vulnerability.xlsx"
    join_csvs(directory_path, output_file_path)
