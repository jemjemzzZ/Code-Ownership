import csv, os, json, ast, time
import pandas as pd

# import from utils
import sys
sys.path.append('../')
from utils import github_api
from utils import nvd_api


"""
process the url link to a list of component links
"""
def process_url_to_dataset(url, cve_id, dataset):
    # dataset setup
    if not os.path.exists(dataset):
        header_df = pd.DataFrame(columns=["Repo User", "Repo Name", "Filename", "Date", "URL", "CVE ID", "CVE Severity"])
        header_df.to_csv(dataset, index=False)
    
    # get cve severity
    cve_severity = nvd_api.get_severity(cve_id)
    
    # get details from commit url
    repo_user, repo_name, commit_sha = github_api.extract_repo_commit(url)
    if repo_user and repo_name and commit_sha:
        files, date = github_api.get_commit_data(url)
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
    
    # get details from pull request url
    repo_user, repo_name, pr_number = github_api.extract_repo_and_pr_number(url)
    if repo_user and repo_name and pr_number:
        files, date = github_api.get_pr_data(url)
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


"""
Fetch results from input file to destination dataset.
row_start_number: is used to cooldown the process
"""
def process_vulnerability_to_dataset(input_file, dataset, row_start_number):
    # rows need to be passed
    row_number = 0
    
    try:
        df = pd.read_excel(input_file, engine='openpyxl')
        for index, row in df.iterrows():
            # skip row before the start row
            if row_number < row_start_number:
                row_number += 1
                continue
            
            # url and cve_id info
            patch_urls = row['Patch URLs']
            cve_id = None if pd.isna(row['CVE ID']) else row['CVE ID']
            
            # skip row with empty urls
            if pd.isna(patch_urls):
                row_number += 1
                continue
            
            # update the dataset
            url_list = ast.literal_eval(patch_urls)
            for url in url_list:
                process_url_to_dataset(url, cve_id, dataset)
            
            row_number += 1 # move to next row
        
        # finish the fetching
        return -1
    except github_api.RateLimitException as e:
        # RATE LIMIT
        print(f"Row Number: {row_number}")
        return row_number # return current fetched rows number

"""
Data collection API,
has a cooldown embedded
"""
def data_collection_api(input_file, destination_dataset):
    # start from 0
    row_start_number = 0
    
    # start fetching
    row_start_number = process_vulnerability_to_dataset(input_file, destination_dataset, row_start_number)
    
    # cooldown
    while row_start_number != -1:
        print(f"API Cooldown. Current fetching: {row_start_number}")
        time.sleep(3600) # sleep 1hr
        row_start_number = process_vulnerability_to_dataset(input_file, destination_dataset, row_start_number)
        


# Test
if __name__ == "__main__":
    data_collection_api("data/vulnerability.xlsx", "data/dataset.csv")