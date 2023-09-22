import pandas as pd

# clear duplication
# df = pd.read_csv('results.csv')
# df = df.drop_duplicates(subset=['URL', 'Name'], keep='first')
# df.to_csv('results.csv', index=False)


# join two cves
A = pd.read_csv('old_cve_results.csv')
B = pd.read_csv('new_cve_results.csv')
unique_B = B[~B.set_index(['URL', 'Name']).index.isin(A.set_index(['URL', 'Name']).index)]
merged_df = pd.concat([A, unique_B], ignore_index=True)
merged_df.to_csv('cve_results.csv', index=False)
