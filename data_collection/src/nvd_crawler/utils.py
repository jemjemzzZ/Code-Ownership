import json, os, re, requests
import pandas as pd


class JSONParser:
    def __init__(self, raw_dir, distilled_dir):
        self.json_dir = raw_dir
        self.csv_dir = distilled_dir

    def parse(self, framework):
        json_dir = self.json_dir + f'nvd_{framework}.json'
        csv_dir  = self.csv_dir  + f'nvd_{framework}.csv'

        with open(json_dir, 'r') as f:
            # setup header
            if not os.path.exists(csv_dir):
                header_df = pd.DataFrame(columns=["Framework", "CVE ID", "Reference URLs", 'Patch URLs'])
                header_df.to_csv(csv_dir, index=False)
                
            # json data
            json_data = json.loads(f.read())
            
            # CVE block
            for data in json_data['vulnerabilities']:
                # cve data
                cve_data = None
                try:
                    cve_data = data['cve']
                except:
                    continue
                
                # cve id
                cve_id = None
                try:
                    cve_id = cve_data['id']
                except:
                    pass
                
                # reference urls
                reference_urls = []
                try:
                    for reference in cve_data['references']:
                        reference_url = reference['url']
                        reference_urls.append(reference_url)
                except:
                    pass
                
                # patch urls
                patch_urls = []
                try:
                    patch_urls = github_utils(reference_urls)
                except:
                    pass

                # write to csv
                df = pd.DataFrame({
                    "Framework": [framework],
                    "CVE ID": [cve_id],
                    "Reference URLs": [reference_urls],
                    'Patch URLs': [patch_urls]
                })
                df.to_csv(csv_dir, mode='a', header=False, index=False)
                
        return


"""
Commit URL crawler
"""
def github_utils(reference_urls):
    patch_urls = []
    
    for url in reference_urls:
        if "/commit/" in url and "/pull/" not in url:
            patch_urls.append(url)
        elif "/commit/" not in url and "/pull/" in url:
            patch_urls.append(url)
    
    if len(patch_urls) != 0:
        return patch_urls
    
    for url in reference_urls:
        if "/blob/" in url or "/security/advisories/" in url:
            # Extract repo_user and repo_name from the URL
            repo_info_match = re.search(r'https://github.com/([^/]+)/([^/]+)/', url)
            if not repo_info_match:
                continue
            repo_user, repo_name = repo_info_match.groups()

            response = requests.get(url)
            response.raise_for_status()

            # Create a regex pattern using the extracted repo_user and repo_name
            pattern = r'https://github.com/{}/{}/commit/[a-f0-9]+\\?"'.format(repo_user, repo_name)
            match = re.search(pattern, response.text)

            if match:
                patch_url = match.group(0).replace("\\", '').replace('"', '')
                if patch_url not in patch_urls:
                    patch_urls.append(patch_url)
        elif "/pull/" in url and "/commits/" in url:
            # Extract repo and commit hash from the URL
            repo, _, commit_hash = url.replace('https://github.com/', '').partition('/pull/')
            commit_hash = re.search(r"/commits/([a-f0-9]{40})", url).group(1)

            patch_url = f"https://github.com/{repo}/commit/{commit_hash}"
            if patch_url not in patch_urls:
                    patch_urls.append(patch_url)
    
    return patch_urls


# Test
if __name__ == "__main__":
    urls = [
        "https://github.com/tensorflow/tensorflow/blob/master/tensorflow/security/advisory/tfsa-2018-002.md",
        "https://github.com/tensorflow/tensorflow/security/advisories/GHSA-977j-xj7q-2jr9",
        "https://github.com/tensorflow/tensorflow/pull/42143/commits/3ade2efec2e90c6237de32a19680caaa3ebc2845"
    ]
    github_utils(urls)
