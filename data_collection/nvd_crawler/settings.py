API_KEY = "0afc16b9-0b01-4f98-994b-691a650918ea"

APP_CONFIG = {
	"distilled_dir":"../data/distilled/",
	"raw_dir":"../data/raw/",
    'frameworks': ['tensorflow','caffe','keras','opencv','pytorch'],
    'nvd_search_api': "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=",
    'headers': {"apiKey": API_KEY},
}