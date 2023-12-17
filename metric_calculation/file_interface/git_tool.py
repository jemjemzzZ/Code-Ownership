import os, re, git, subprocess, time
from datetime import datetime

# import from utils
import sys
sys.path.append('../')
from utils import metric_api


"""
Clone the git by repo_user+repo_name,
or from existing repos folder
"""
def git_get_repo(repo_user, repo_name):
    repo_dir = f"../repos/{repo_name}_repo" # local repo address
    
    if not os.path.exists(repo_dir):
        # clone from external link
        repo_url = f"https://github.com/{repo_user}/{repo_name}.git"
        repo = git.Repo.clone_from(repo_url, repo_dir)
    else:
        # clone from existing directory
        repo = git.Repo(repo_dir)
    return repo, repo_dir


"""
Close the GitPython tool and absort the git repo
"""
def git_close_repo(repo, repo_dir):
    repo.close()
    time.sleep(2)
    # subprocess.run(['taskkill', '/F', '/IM', 'git.exe'], shell=True)
    git.rmtree(f"../repos/{repo_dir}/.git/")
    git.rmtree(repo_dir) # remove local repo
    return


"""
Get the repo list of dates info from git log
"""
def git_get_repo_date(repo, repo_dir):
    repo_git = git.Git(repo.working_tree_dir)
    repo_time_flags = ["--reverse", "--pretty=format:'%h %cd'", "--date=iso"]
    repo_time = repo_git.log(*repo_time_flags)
    return repo_time


"""
Calculate repo existing time till the input commit time
"""
def calculate_days(repo_time, iso_date):
    repo_time_formatted = repo_time.splitlines()
    time_string1 = repo_time_formatted[0] # start date
    time_string2 = iso_date # commit time (end date)
    
    # Extract datetime objects from the time strings
    datetime_obj1 = datetime.strptime(time_string1.split()[1] + ' ' + time_string1.split()[2], "%Y-%m-%d %H:%M:%S")
    datetime_obj2 = datetime.strptime(time_string2, "%Y-%m-%dT%H:%M:%SZ")

    # Calculate the time difference
    time_difference = datetime_obj2 - datetime_obj1
    number_of_days = time_difference.days
    return number_of_days


"""
Get the license info from the git repo
"""
def git_get_repo_license(repo, repo_dir):
    repo_git = git.Git(repo.working_tree_dir)
    license_files = [filename for filename in repo.git.ls_files().splitlines() if "license" in filename.lower()]
    repo_license = ""
    if len(license_files) > 0:
        license_file = f"{repo_dir}/" + license_files[0]
        with open(license_file, 'r') as file:
            repo_license = file.read()
    return repo_license


"""
Check the license category
"""
def calculate_repo_license_info(repo_license):
    license_types = ["Apache", "GNU GENERAL PUBLIC", "MIT", "BSD 2-Clause", "BSD 3-Clause", 
                     "Boost Software", "Creative Commons Legal Code", "Eclipse Public", 
                     "GNU AFFERO GENERAL PUBLIC", "GNU LESSER GENERAL PUBLIC", "Mozilla Public", 
                     "Unlicense"]
    for license_type in license_types:
        if license_type.lower() in repo_license.lower():
            return license_type
    return None


"""
Get the repo releases from the creation day to the input date
"""
def git_get_repo_release(repo, iso_date):
    repo_git = git.Git(repo.working_tree_dir)
    date_limit_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ") # the end date
    
    repo_release_flags = ["-l", "v*"]
    tags = repo_git.tag(*repo_release_flags).splitlines()
    repo_release = {}
    for tag in tags:
        tag_date = repo_git.show("-s", "--format=%ci", tag)
        tag_date_obj = datetime.strptime(tag_date.split()[0] + " " + tag_date.split()[1], "%Y-%m-%d %H:%M:%S")
        # within end date
        if tag_date_obj <= date_limit_obj:
            repo_release[tag] = tag_date
    return repo_release


"""
Get the repo release within the days to the input date
"""
def git_get_repo_release_within_age(repo, iso_date, age):
    repo_git = git.Git(repo.working_tree_dir)
    date_limit_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ") # the end date
    
    repo_release_flags = ["-l", "v*"]
    tags = repo_git.tag(*repo_release_flags).splitlines()
    repo_release_age = {}
    for tag in tags:
        tag_date = repo_git.show("-s", "--format=%ci", tag)
        tag_date_obj = datetime.strptime(tag_date.split()[0] + " " + tag_date.split()[1], "%Y-%m-%d %H:%M:%S")
        # (end date - age : end date)
        if (date_limit_obj - tag_date_obj).days <= age and tag_date_obj <= date_limit_obj:
            repo_release_age[tag] = tag_date
    return repo_release_age


"""
Extract the release details from repo release log
!!! Support pytorch and tensorflow only
"""
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

    return (major, minor, pre_release, patch, alpha_beta)


"""
Get the commit history of filename within the input date
"""
def git_get_file_history(repo, filename, iso_date):
    git_date_format = iso_date.replace('T', '').replace('Z', '')
    file_history = repo.git.log('--follow', "--stat", 
                            "--pretty=format:'commit %h%nAuthor: %aN <%aE>%nDate: %ad%n'", 
                            "--date=iso", '-p', '--', filename, before=git_date_format)
    return file_history


"""
Create the Metric model from Git Repo
"""
def create_component(repo_user, repo_name, filename, iso_date):
    # initialise the component
    component = metric_api.Component(f"{repo_name}/{filename}", "file")
    
    # GitPython repo info
    repo, repo_dir = git_get_repo(repo_user, repo_name)
    repo_time = git_get_repo_date(repo, repo_dir)
    repo_day_difference = calculate_days(repo_time, iso_date)
    repo_license = git_get_repo_license(repo, repo_dir)
    repo_license_info = calculate_repo_license_info(repo_license)
    repo_release = git_get_repo_release(repo, iso_date)
    repo_release_info = calculate_repo_release(repo_release)
    
    # File commit history
    file_history = git_get_file_history(repo, filename, iso_date)
    
    # Code ownership metric
    blocks = re.split(r'commit [0-9a-f]+\n', file_history)[1:] # one commit in one block
    for block in blocks:
        # extract author and date
        author_match = re.search(r'Author:\s+(.*)', block)
        if author_match:
            author = author_match.group(1)
        date_match = re.search(r'Date:\s+(.*)', block)
        if date_match:
            date = date_match.group(1)
        
        # add contribute as 1 (paper info)
        component.addContribute(author, 1)
    
    # time/release/license metric
    timeType, ossStage = metric_api.calculateTime(repo_day_difference, repo_release_info, repo_time, repo_release)
    licenseType = metric_api.checkLicenseType(repo_license_info)
    component.setTime(repo_day_difference, repo_release_info, timeType, ossStage)
    component.setLicense(repo_license_info, licenseType)
    
    # time/release metric by file lifetime
    age = calculate_age(file_history)
    repo_release_age = git_get_repo_release_within_age(repo, iso_date, age)
    repo_release_info_age = calculate_repo_release(repo_release_age)
    timeTypeAge, ossStageAge = metric_api.calculateTime(age, repo_release_info_age, repo_time, repo_release_age)
    component.setTimeAge(age, repo_release_info_age, timeTypeAge, ossStageAge)
    
    # check pre-/post- release
    prepost = metric_api.checkPrePostRelease(repo_release)
    component.setPrePost(prepost)
    
    # classic code metric
    total_added, total_deleted = calculate_churn(filename, file_history)
    file_size = get_filesize(repo, filename, file_history)
    component.setClassic(total_added, total_deleted, file_size)
    
    # Finalise the component
    component.calculateOwnership()
    
    return component


"""
Calculate code churn info based on commit history
"""
def calculate_churn(filename, file_history):
    total_added = 0
    total_deleted = 0

    try:
        # one commit in one block
        blocks = re.split(r'commit [0-9a-f]+\n', file_history)[1:]
        for block in blocks:
            # lines change
            insertion_pattern = r'(\d+) insertion'
            deletion_pattern = r'(\d+) deletion'
            
            insertion_match = re.search(insertion_pattern, block)
            deletion_match = re.search(deletion_pattern, block)

            insertions = int(insertion_match.group(1)) if insertion_match else 0
            deletions = int(deletion_match.group(1)) if deletion_match else 0

            total_added += insertions
            total_deleted += deletions
    except Exception as e:
        total_added = 0
        total_deleted = 0
        print(e)
    
    return total_added, total_deleted


"""
Calculate the file length by lines ammount
"""
def get_filesize(repo, filename, file_history):
    filesize = 0
    
    try:
        lines = file_history.split("\n")
        commit_hashes = [line.split()[1] for line in lines if line.startswith("'commit")]
        latest_commit_hash = commit_hashes[0] # get the latest commit hash
        file_content = repo.git.show(f"{latest_commit_hash}:{filename}")
        filesize = len(file_content.split('\n'))
    except Exception as e:
        print(filename)
        print(e)
    
    return filesize


"""
Calculate the file lifetime based on commit history
"""
def calculate_age(file_history):
    age = 0
    
    # one commit in one block
    blocks = re.split(r'commit [0-9a-f]+\n', file_history)[1:]
    date1_match = re.search(r'Date:\s+(.*)', blocks[0])
    date2_match = re.search(r'Date:\s+(.*)', blocks[-1])
    
    if date1_match and date2_match:
        date1 = date1_match.group(1) # latest date
        date2 = date2_match.group(1) # start date
        
        datetime_obj1 = datetime.strptime(date1.split()[0] + ' ' + date1.split()[1], "%Y-%m-%d %H:%M:%S")
        datetime_obj2 = datetime.strptime(date2.split()[0] + ' ' + date2.split()[1], "%Y-%m-%d %H:%M:%S")
        
        # Calculate the time difference
        time_difference = datetime_obj1 - datetime_obj2
        age = time_difference.days
    
    return age


# Test
if __name__ == "__main__":
    repo_user = "tensorflow"
    repo_name = "tensorflow"
    filename = "tensorflow/core/kernels/sparse_tensors_map_ops.cc"
    iso_date = "2021-12-09T22:32:48Z"
    component = create_component(repo_user, repo_name, filename, iso_date)
    component.outputMessage()
