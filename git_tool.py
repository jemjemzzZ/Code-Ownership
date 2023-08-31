import os, re, sys, git, subprocess, time
from datetime import datetime
from metric_process import *

import os, re, sys, git, subprocess, time
from datetime import datetime
from metric_process import *


def git_get_repo(repo_user, repo_name):
    repo_dir = f"repos/{repo_name}_repo"
    
    if not os.path.exists(repo_dir):
        repo_url = f"https://github.com/{repo_user}/{repo_name}.git"
        repo = git.Repo.clone_from(repo_url, repo_dir)
    else:
        repo = git.Repo(repo_dir)
    return repo, repo_dir


def git_close_repo(repo, repo_dir):
    repo.close()
    time.sleep(2)
    # subprocess.run(['taskkill', '/F', '/IM', 'git.exe'], shell=True)
    git.rmtree(f"{repo_dir}/.git/")
    git.rmtree(repo_dir) # remove local repo
    return


def git_get_repo_date(repo, repo_dir):
    repo_git = git.Git(repo.working_tree_dir)
    repo_time_flags = ["--reverse", "--pretty=format:'%h %cd'", "--date=iso"]
    repo_time = repo_git.log(*repo_time_flags)
    return repo_time


def calculate_days(repo_time, iso_date):
    repo_time_formatted = repo_time.splitlines()
    time_string1 = repo_time_formatted[0] # start date
    time_string2 = iso_date # commit time
    # Extract datetime objects from the time strings
    datetime_obj1 = datetime.strptime(time_string1.split()[1] + ' ' + time_string1.split()[2], "%Y-%m-%d %H:%M:%S")
    datetime_obj2 = datetime.strptime(time_string2, "%Y-%m-%dT%H:%M:%SZ")

    # Calculate the time difference
    time_difference = datetime_obj2 - datetime_obj1
    number_of_days = time_difference.days
    return number_of_days


def git_get_repo_license(repo, repo_dir):
    repo_git = git.Git(repo.working_tree_dir)
    license_files = [filename for filename in repo.git.ls_files().splitlines() if "license" in filename.lower()]
    repo_license = ""
    if len(license_files) > 0:
        license_file = f"{repo_dir}/" + license_files[0]
        with open(license_file, 'r') as file:
            repo_license = file.read()
    return repo_license


def calculate_repo_license_info(repo_license):
    license_types = ["Apache", "GNU GENERAL PUBLIC", "MIT", "BSD 2-Clause", "BSD 3-Clause", 
                     "Boost Software", "Creative Commons Legal Code", "Eclipse Public", 
                     "GNU AFFERO GENERAL PUBLIC", "GNU LESSER GENERAL PUBLIC", "Mozilla Public", 
                     "Unlicense"]
    for license_type in license_types:
        if license_type.lower() in repo_license.lower():
            return license_type
    return None


def git_get_repo_release(repo, iso_date):
    repo_git = git.Git(repo.working_tree_dir)
    date_limit_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    repo_release_flags = ["-l", "v*"]
    tags = repo_git.tag(*repo_release_flags).splitlines()
    repo_release = {}
    for tag in tags:
        tag_date = repo_git.show("-s", "--format=%ci", tag)
        tag_date_obj = datetime.strptime(tag_date.split()[0] + " " + tag_date.split()[1], "%Y-%m-%d %H:%M:%S")
        if tag_date_obj <= date_limit_obj:
            repo_release[tag] = tag_date
    return repo_release


def calculate_repo_release(repo_release):
    major = 0 # major release
    minor = 0 # minor release
    pre_release = 0 # release candidate
    patch = 0 # patch release
    alpha_beta = 0 # alpha beta 

    for tag, date in repo_release.items():
        release = tag.split(".")
        if len(release) < 3:
            continue
        
        if "rc" in release[2]:
            pre_release += 1
        elif "a" in release[2] or "b" in release[2]:
            alpha_beta += 1
        elif release[2].isdigit() and int(release[2]) > 0:
            patch += 1
        elif int(release[1]) > 0:
            minor += 1
        else:
            major += 1
    # print((major, minor, pre_release, patch, alpha_beta))
    return (major, minor, pre_release, patch, alpha_beta)


def git_get_file_history(repo, filename, iso_date):
    git_date_format = iso_date.replace('T', '').replace('Z', '')
    file_history = repo.git.log('--follow', "--numstat", 
                            "--pretty=format:'commit %h%nAuthor: %aN <%aE>%nDate: %ad%n'", 
                            "--date=iso", '-p', '--', filename, before=git_date_format)
    # print(file_history)
    return file_history


def create_component(repo_user, repo_name, filename, iso_date):
    component = Component(f"{repo_name}/{filename}", "file")
    
    repo, repo_dir = git_get_repo(repo_user, repo_name)
    repo_time = git_get_repo_date(repo, repo_dir)
    repo_day_difference = calculate_days(repo_time, iso_date)
    repo_license = git_get_repo_license(repo, repo_dir)
    repo_license_info = calculate_repo_license_info(repo_license)
    repo_release = git_get_repo_release(repo, iso_date)
    repo_release_info = calculate_repo_release(repo_release)
    
    file_history = git_get_file_history(repo, filename, iso_date)
    blocks = re.split(r'commit [0-9a-f]+\n', file_history)[1:]
    for block in blocks:
        # extract author and date
        author_match = re.search(r'Author:\s+(.*)', block)
        if author_match:
            author = author_match.group(1)
        date_match = re.search(r'Date:\s+(.*)', block)
        if date_match:
            date = date_match.group(1)
        # print(f"Author: {author}")
        # print(f"Date: {date}")
        component.addContribute(author, 1)
    
    timeType, ossStage = calculateTime(repo_day_difference, repo_release_info, repo_time, repo_release)
    licenseType = checkLicenseType(repo_license_info)
    component.setTime(repo_day_difference, repo_release_info, timeType, ossStage)
    component.setLicense(repo_license_info, licenseType)
    component.calculateOwnership()
    # print(f"Days: {repo_day_difference}")
    # print(f"Release: {repo_release_info}")
    # print(f"Stage: {timeType}, {ossStage}")
    # print(f"License: {repo_license_info}, {licenseType}")
    return component


# repo_user = "tensorflow"
# repo_name = "tensorflow"
# filename = "tensorflow/core/kernels/sparse_tensors_map_ops.cc"
# iso_date = "2021-12-09T22:32:48Z"
# create_component(repo_user, repo_name, filename, iso_date)
