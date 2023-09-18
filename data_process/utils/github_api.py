import re
import requests


"""
TOKEN used for Github
"""
TOKEN = "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"
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'User-Agent': 'Code Ownership'
}


"""
Rate limit error to stall the execution
"""
class RateLimitException(Exception):
    pass


"""
Extract the repo commit from URL
"""
def extract_repo_commit(url):
    # Extract repository name and pull request number from the URL
    pattern = r"https://github.com/([^/]+)/([^/]+)/commit/([a-f0-9]+)/?"
    match = re.match(pattern, url)
    
    if match:
        repo_user, repo_name, commit_sha = match.groups()
        return repo_user, repo_name, commit_sha
    else:
        return None, None, None


"""
Get all files from commit link
"""
def get_commit_files(commit_url):
    files = []
    date = None
    
    # get github api response
    commit_response = requests.get(commit_url, headers=HEADERS)
    if commit_response.status_code == 200:
        # data process
        commit_data = commit_response.json()
        commit_date = commit_data['commit']['author']['date']
        date = commit_date
        
        # Get the list of modified files in the commit
        files_data = commit_data['files']
        for file_data in files_data:
            file_path = file_data['filename']
            files.append(file_path)
    else:
        print(commit_url)
        print(f"Failed to fetch commit information: {commit_response.status_code}")
        print(commit_response.json().get('message', 'Unknown error'))
        # RATE LIMIT
        if commit_response.status_code == 403 and check_rate_limit() <= 0:
            raise RateLimitException()
        
    return files, date


"""
Get the commit details (files, date) from commit url
"""
def get_commit_data(commit_url):
    repo_user, repo_name, commit_sha = extract_repo_commit(commit_url)
    commit_working_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/commits/{commit_sha}"
    return get_commit_files(commit_working_url)


"""
Extract repo info and pull request number from pr link
"""
def extract_repo_and_pr_number(url):
    # Extract repository name and pull request number from the URL
    pattern = r"https://github.com/([^/]+)/([^/]+)/pull/(\d+)/?"
    match = re.match(pattern, url)
    
    if match:
        repo_user, repo_name, pr_number = match.groups()
        return repo_user, repo_name, int(pr_number)
    else:
        return None, None, None


"""
Get the details (files, date) from pull request url
"""
def get_pr_data(pull_request_url):
    files = []
    date = None
    
    # extract repo info
    repo_user, repo_name, pr_number = extract_repo_and_pr_number(pull_request_url)
    
    # get github api response
    if repo_user and repo_name and pr_number:
        pr_info_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/pulls/{pr_number}"
        response = requests.get(pr_info_url, headers=HEADERS)
        if response.status_code == 200:
            # pr data process
            pull_request_data = response.json()
            head_commit_sha = pull_request_data['head']['sha']
            created_at = pull_request_data['created_at']
            date = created_at

            # Fetch commits associated with the pull request using GitHub API
            commits_url = pull_request_data['commits_url']
            commits_response = requests.get(commits_url, headers=HEADERS)
            if commits_response.status_code == 200:
                # commits data process
                commits_data = commits_response.json()
                for commit in commits_data:
                    commit_sha = commit['sha']
                    commit_message = commit['commit']['message']

                    # Fetch commit details using GitHub API
                    commit_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/commits/{commit_sha}"
                    commit_files, commit_date = get_commit_files(commit_url)
                    for commit_file in commit_files:
                        if commit_file not in files:
                            files.append(commit_file)
            else:
                print(commits_url)
                print(f"Failed to fetch commits information: {commits_response.status_code}")
                print(commits_response.json().get('message', 'Unknown Error'))
                # RATE LIMIT
                if commits_response.status_code == 403 and check_rate_limit() <= 0:
                    raise RateLimitException()
        else:
            print(pr_info_url)
            print(f"Failed to fetch pull request information: {response.status_code}")
            print(response.json().get('message', 'Unknown error'))
            # RATE LIMIT
            if response.status_code == 403 and check_rate_limit() <= 0:
                raise RateLimitException()
    else:
        print("Invalid pull request URL.")
        
    return files, date

"""
Check the github rate limit left
"""
def check_rate_limit():
    response = requests.get('https://api.github.com/user', headers=HEADERS)
    remaining = response.headers.get('X-Ratelimit-Remaining')
    # print(f"Requests remaining: {remaining}")
    return int(remaining)


# Test
if __name__ == "__main__":
    pull_request_url = "https://github.com/tensorflow/tensorflow/pull/6221"
    pr_data = get_pr_data(pull_request_url)
    print(pr_data)
    print("############################################################")
    commit_url = "https://github.com/tensorflow/tensorflow/commit/b51b82fe65ebace4475e3c54eb089c18a4403f1c"
    commit_data = get_commit_data(commit_url)
    print(commit_data)
