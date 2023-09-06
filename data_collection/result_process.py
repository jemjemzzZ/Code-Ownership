from metric_process import *
from git_tool import *

import csv, os, json, ast
import pandas as pd


def write_component_to_results(filename, component_tuple):
    file_exist_flag = True
    if not os.path.exists(filename):
        file_exist_flag = False
    
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        if not file_exist_flag:
            # header
            header = ["URL", "Repo Name", "Date", 
                      "Name", "Component Type", "Ownership", "Num of Contributor", 
                      "Num of Minor 5%", "Per of Minor 5%", "Avg of Minor Contri 5%", 
                      "Num of Minor 10%", "Per of Minor 10%", "Avg of Minor Contri 10%", 
                      "Num of Minor 20%", "Per of Minor 20%", "Avg of Minor Contri 20%", 
                      "Num of Minor 50%", "Per of Minor 50%", "Avg of Minor Contri 50%", 
                      "Days Difference", "Release Info", "Time Stage", "Oss Stage", 
                      "License Info", "License Type", 
                      "Total Added", "Total Deleted", "File Size"]
            csv_writer.writerow(header)
        
        url = component_tuple[3]
        date = component_tuple[2]
        repo_name = component_tuple[1]
        component = component_tuple[0]
        
        row = [url, repo_name, date, 
                component.name, component.componentType, component.ownership, component.contributorNum, 
                component.minorNum5, component.minorPer5, component.minorContriAvg5, 
                component.minorNum10, component.minorPer10, component.minorContriAvg10, 
                component.minorNum20, component.minorPer20, component.minorContriAvg20, 
                component.minorNum50, component.minorPer50, component.minorContriAvg50, 
                component.time, json.dumps(component.release), component.timeType, component.ossStage, 
                component.licenseInfo, component.licenseType, 
                component.total_added, component.total_deleted, component.filesize]
        csv_writer.writerow(row)
        
    return


def process_dataset_to_results(dataset, result_file):
    df = pd.read_csv(dataset)
    # Traverse each row
    for index, row in df.iterrows():
        repo_user = row["Repo User"]
        repo_name = row["Repo Name"]
        filename = row["Filename"]
        date = row["Date"]
        url = row["URL"]
        
        try:
            component = create_component(repo_user, repo_name, filename, date)
            component_tuple = (component, repo_name, date, url)
            write_component_to_results(result_file, component_tuple)
        except Exception as e:
            print(f"{repo_name}/{filename}")
            print(f"{url}")
            print(e)
            print("")


process_dataset_to_results("data/dataset.csv", "data/results.csv")