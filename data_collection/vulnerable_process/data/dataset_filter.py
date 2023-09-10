import pandas as pd


def filter_out_cve(raw_dataset, new_dataset):
    df = pd.read_csv(raw_dataset)

    filtered_df = df.dropna(subset=['CVE ID', 'CVE Severity'])
    filtered_df = filtered_df[(filtered_df['CVE ID'] != '') & (filtered_df['CVE Severity'] != '')]

    filtered_df.to_csv(new_dataset, index=False)


def filter_out_pytorch_tensorflow(raw_dataset, new_dataset):
    df = pd.read_csv(raw_dataset)
    
    allowed_repo_names = ["pytorch", "tensorflow"]
    filtered_df = df[df['Repo Name'].isin(allowed_repo_names)]
    
    filtered_df.to_csv(new_dataset, index=False)
    
    
filter_out_cve("dataset.csv", "cve_dataset.csv")
filter_out_pytorch_tensorflow("dataset.csv", "pytorch_tensorflow_dataset.csv")
