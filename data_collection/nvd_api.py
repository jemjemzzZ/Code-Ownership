import requests
import json
import time

API_KEY = "0afc16b9-0b01-4f98-994b-691a650918ea"
HEADERS = {"apiKey": API_KEY}


def get_severity(cve_id):
    if cve_id == None:
        return None
    
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        time.sleep(60)
        response = requests.get(url, headers=HEADERS)
    
    data = response.json()
    # severity = data['vulnerabilities'][0]['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']
    metric_keys = [key for key in data['vulnerabilities'][0]['cve']['metrics'].keys()]
    if metric_keys:
        severity = data['vulnerabilities'][0]['cve']['metrics'][metric_keys[0]][0]['cvssData']['baseScore']
        return severity
    
    return None

# print(get_severity("CVE-2017-17760"))
# print(get_severity("CVE-2020-15266"))
# print(get_severity("CVE-2022-41893"))
# print(get_severity("CVE-2018-8825"))
# print(get_severity("CVE-2018-10055"))
# print(get_severity("CVE-2017-12601"))
# print(get_severity("CVE-2016-10658"))