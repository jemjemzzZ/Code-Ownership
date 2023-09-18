import csv, os, re, json, ast
import pandas as pd

import git_tool

# import from utils
import sys
sys.path.append('../')
from utils import metric_api


"""
Extract the repo by URL
"""
def extract_repo(url):
    # Extract repository name and pull request number from the URL
    pattern = r"https://github.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    
    if match:
        repo_user, repo_name = match.groups()
        return repo_user, repo_name
    else:
        return None, None


"""
Write the component to the destination file
"""
def write_component_to_results(filename, url, repo_name, component):
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
            header = ["URL", "Repo Name", 
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
        
        # write row
        row = [url, repo_name, 
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
Create components from URL,
put component info to destination result file
"""
def data_process_api(url, result_file):
    # repo
    repo_user, repo_name = extract_repo(url)
    # files in repo
    filenames = git_tool.get_filenames(repo_user, repo_name)
    
    for filename in filenames:
        try:
            # create component
            component = git_tool.create_component(repo_user, repo_name, filename)
            # set component as non-vulernable
            component.setIsDefective(False)
            # write to result file
            write_component_to_results(result_file, url, repo_name, component)
        except Exception as e:
            print(f"{repo_name}/{filename}")
            print(e)
            print("")
    
    return 


# Test
if __name__ == "__main__":
    data_process_api("https://github.com/phwl/pyverilator", "data/non_vulnerable_results.csv")
    # data_process_api("https://github.com/tensorflow/tensorflow", "data/non_vulnerable_results.csv")
    # data_process_api("https://github.com/pytorch/pytorch", "data/non_vulnerable_results.csv")