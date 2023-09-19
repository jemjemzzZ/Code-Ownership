import json, os
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
                header_df = pd.DataFrame(columns=["Framework", "CVE ID", "Reference URLs"])
                header_df.to_csv(csv_dir, index=False)
                
            # json data
            json_data = json.loads(f.read())
            
            # CVE block
            for data in json_data['vulnerabilities']:
                cve_data = None
                try:
                    cve_data = data['cve']
                except:
                    continue
                
                cve_id = None
                try:
                    cve_id = cve_data['id']
                except:
                    pass
                
                reference_urls = []
                try:
                    for reference in cve_data['references']:
                        reference_url = reference['url']
                        reference_urls.append(reference_url)
                except:
                    pass
                
                df = pd.DataFrame({
                    "Framework": [framework],
                    "CVE ID": [cve_id],
                    "Reference URLs": [reference_urls]
                })
                df.to_csv(csv_dir, mode='a', header=False, index=False)
                
        return
