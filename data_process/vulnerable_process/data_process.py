import csv, os, json, ast
import pandas as pd

import git_tool

# import from utils
import sys
sys.path.append('../')
from utils import metric_api


"""
Write the component from component tuple to the destination file
"""
def write_component_to_results(filename, component_tuple):
    # check file location
    file_exist_flag = True
    if not os.path.exists(filename):
        file_exist_flag = False
    
    # open file
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # file creation
        if not file_exist_flag:
            # header
            header = ["URL", "Repo Name", "Date", "CVE ID", "CVE Severity", 
                      "Name", "Component Type", "Ownership", "Num of Contributor", 
                      "Num of Minor 5%", "Per of Minor 5%", "Avg of Minor Contri 5%", 
                      "Num of Minor 10%", "Per of Minor 10%", "Avg of Minor Contri 10%", 
                      "Num of Minor 20%", "Per of Minor 20%", "Avg of Minor Contri 20%", 
                      "Num of Minor 50%", "Per of Minor 50%", "Avg of Minor Contri 50%", 
                      "Days Difference", "Release Info", "Time Stage", "Oss Stage", 
                      "Age", "Release Info Aged", "Time Stage Aged", "Oss Stage Aged", 
                      "License Info", "License Type", 
                      "Total Added", "Total Deleted", "File Size", 
                      "Is Defective"]
            csv_writer.writerow(header)
        
        # extract data from component tuple
        cve_severity = component_tuple[5]
        cve_id = component_tuple[4]
        url = component_tuple[3]
        date = component_tuple[2]
        repo_name = component_tuple[1]
        component = component_tuple[0]
        
        # write row
        row = [url, repo_name, date, cve_id, cve_severity, 
                component.name, component.componentType, component.ownership, component.contributorNum, 
                component.minorNum5, component.minorPer5, component.minorContriAvg5, 
                component.minorNum10, component.minorPer10, component.minorContriAvg10, 
                component.minorNum20, component.minorPer20, component.minorContriAvg20, 
                component.minorNum50, component.minorPer50, component.minorContriAvg50, 
                component.time, json.dumps(component.release), component.timeType, component.ossStage, 
                component.age, json.dumps(component.releaseAge), component.timeTypeAge, component.ossStageAge, 
                component.licenseInfo, component.licenseType, 
                component.total_added, component.total_deleted, component.filesize, 
                component.isDefective]
        csv_writer.writerow(row)
        
    return


"""
Create components from dataset,
put component info to destination result file
"""
def data_process_api(dataset, result_file):
    df = pd.read_csv(dataset)
    
    # iterate each row of dataset
    for index, row in df.iterrows():
        # data fetch
        repo_user = row["Repo User"]
        repo_name = row["Repo Name"]
        filename = row["Filename"]
        date = row["Date"]
        url = row["URL"]
        cve_id = row["CVE ID"]
        cve_severity = row["CVE Severity"]
        
        try:
            # create component
            component = git_tool.create_component(repo_user, repo_name, filename, date)
            # set component as vulernable
            component.setIsDefective(True)
            # write to result file
            component_tuple = (component, repo_name, date, url, cve_id, cve_severity)
            write_component_to_results(result_file, component_tuple)
        except Exception as e:
            # process exception
            print(f"{repo_name}/{filename}")
            print(f"{url}")
            print(e)
            print("")


# Test
if __name__ == "__main__":
    data_process_api("data/dataset.csv", "data/results.csv")
    data_process_api("data/cve_dataset.csv", "data/cve_results.csv")
    data_process_api("data/pytorch_tensorflow_dataset.csv", "data/pytorch_tensorflow_results.csv")