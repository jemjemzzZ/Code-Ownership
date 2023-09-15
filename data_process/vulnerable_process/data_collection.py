from github_api import *
from nvd_api import *

import csv, os, json, ast
import pandas as pd


def process_url_to_dataset(url, cve_id, dataset):
    if not os.path.exists(dataset):
        header_df = pd.DataFrame(columns=["Repo User", "Repo Name", "Filename", "Date", "URL", "CVE ID", "CVE Severity"])
        header_df.to_csv(dataset, index=False)
    
    cve_severity = get_severity(cve_id)
    
    repo_user, repo_name, commit_sha = extract_repo_commit(url)
    if repo_user and repo_name and commit_sha:
        files, date = get_commit_data(url)
        for file in files:
            df = pd.DataFrame({
                "Repo User": [repo_user],
                "Repo Name": [repo_name],
                "Filename": [file],
                "Date": [date],
                "URL": [url],
                "CVE ID": [cve_id],
                "CVE Severity": [cve_severity]
            })
            df.to_csv(dataset, mode='a', header=False, index=False)
    
    repo_user, repo_name, pr_number = extract_repo_and_pr_number(url)
    if repo_user and repo_name and pr_number:
        files, date = get_pr_data(url)
        for file in files:
            df = pd.DataFrame({
                "Repo User": [repo_user],
                "Repo Name": [repo_name],
                "Filename": [file],
                "Date": [date],
                "URL": [url],
                "CVE ID": [cve_id],
                "CVE Severity": [cve_severity]
            })
            df.to_csv(dataset, mode='a', header=False, index=False)


def process_vulnerability_to_dataset(input_file, dataset, row_start_number):
    row_number = 0
    try:
        df = pd.read_excel(input_file, engine='openpyxl')
        for index, row in df.iterrows():
            if row_number < row_start_number:
                row_number += 1
                continue
            
            patch_urls = row['Patch URLs']
            cve_id = None if pd.isna(row['CVE ID']) else row['CVE ID']
            
            if pd.isna(patch_urls):
                row_number += 1
                continue
            
            url_list = ast.literal_eval(patch_urls)
            for url in url_list:
                process_url_to_dataset(url, cve_id, dataset)
                
            row_number += 1
    except RateLimitException as e:
        print(f"Row Number: {row_number}")
        return


process_vulnerability_to_dataset("data/vulnerability.xlsx", "data/dataset.csv", 0)