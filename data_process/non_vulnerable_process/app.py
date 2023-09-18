import argparse

import data_process


"""
Default settings for URLs
"""
APP_CONFIG = {
    'result': 'data/non_vulnerable_results.csv',
    'tensorflow': 'https://github.com/tensorflow/tensorflow',
    'pytorch': 'https://github.com/pytorch/pytorch'
}


"""
Command Line interface
"""
def main():
    parser = argparse.ArgumentParser(description='Non_Vulnerable_process Interface')

    # Add arguments
    parser.add_argument('-p', '--process', action='store_true', help='Process the default URLs')
    parser.add_argument('--url', nargs=1, help='Specify the REPO URL', metavar=('URL'))
    parser.add_argument('--dst', nargs=1, help='Specify the result destination', metavar=('Dst'))
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Data Process
    if args.process:
        result_file = args.dst if args.dst else APP_CONFIG['result'] # result file location
        
        # use custom URL
        if args.url:
            url = args.url
            data_process.data_process_api(url, result_file)
            return
        else:
            data_process.data_process_api(APP_CONFIG['tensorflow'], result_file)
            data_process.data_process_api(APP_CONFIG['pytorch'], result_file)
            return
        

# main
if __name__ == "__main__":
    main()