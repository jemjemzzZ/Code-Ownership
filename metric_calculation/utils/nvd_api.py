import requests, json, time
from .github_api import *


"""
NVD API key
"""
API_KEY = "" # replace with ur NVD Token
HEADERS = {"apiKey": API_KEY}


"""
Get the latest cve severity from cve id
"""
def get_severity(cve_id):
    if cve_id == None:
        return None
    
    # get response
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    response = requests.get(url, headers=HEADERS)
    
    # cooldown 60 sec
    if response.status_code != 200:
        time.sleep(60)
        response = requests.get(url, headers=HEADERS)
    
    try:
        data = response.json()
        # get latest cve metrics data
        metric_keys = [key for key in data['vulnerabilities'][0]['cve']['metrics'].keys()]
        if metric_keys:
            severity = data['vulnerabilities'][0]['cve']['metrics'][metric_keys[0]][0]['cvssData']['baseScore']
            return severity
    except Exception as e:
        raise RateLimitException()
    
    return None


# Test
if __name__ == "__main__":
    print(get_severity("CVE-2017-17760"))
    print(get_severity("CVE-2020-15266"))
    print(get_severity("CVE-2022-41893"))
    print(get_severity("CVE-2018-8825"))
    print(get_severity("CVE-2018-10055"))
    print(get_severity("CVE-2017-12601"))
    print(get_severity("CVE-2016-10658"))