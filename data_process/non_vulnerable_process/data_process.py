from metric_process import *
from git_process import *

import csv, os, json, ast
import pandas as pd


def extract_repo(url):
    # Extract repository name and pull request number from the URL
    pattern = r"https://github.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    
    if match:
        repo_user, repo_name = match.groups()
        return repo_user, repo_name
    else:
        return None, None


def write_component_to_results(filename, url, repo_name, component):
    file_exist_flag = True
    if not os.path.exists(filename):
        file_exist_flag = False
    
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
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


def write_url_to_file(url, result_file):
    repo_user, repo_name = extract_repo(url)
    
    filenames = get_filenames(repo_user, repo_name)
    
    for filename in filenames:
        try:
            component = create_component(repo_user, repo_name, filename)
            write_component_to_results(result_file, url, repo_name, component)
        except Exception as e:
            print(e)
    
    return 


write_url_to_file("https://github.com/tensorflow/tensorflow", "data/non_vulnerable_results.csv")
write_url_to_file("https://github.com/pytorch/pytorch", "data/non_vulnerable_results.csv")