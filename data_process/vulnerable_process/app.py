import argparse

import data_collection, data_process


"""
Default settings for files
"""
APP_CONFIG = {
    'vulnerability dataset': 'data/vulnerability.xlsx',
    'dataset': 'data/dataset.csv',
    'result': 'data/results.csv',
    'cve dataset': 'data/cve_dataset.csv',
    'cve result': 'data/cve_results.csv',
    'pytorch tensorflow dataset': 'data/pytorch_tensorflow_dataset.csv',
    'pytorch tensorflow result': 'data/pytorch_tensorflow_results.csv'
}


"""
Command Line interface
"""
def main():
    parser = argparse.ArgumentParser(description='Vulnerable_process Interface')

    # Add arguments
    parser.add_argument('-c', '--collect', action='store_true', help='Collect data from the vulnerability file')
    parser.add_argument('-p', '--process', action='store_true', help='Process the dataset')
    parser.add_argument('--cve', action='store_true', help='Process CVE dataset only')
    parser.add_argument('--torchflow', action='store_true', help='Process Pytorch/Tensorflow dataset only')
    parser.add_argument('--files', nargs=2, help='Input two custom files', metavar=('Src', 'Dst'))
    
    # Parse the arguments
    args = parser.parse_args()

    # Data Collection
    if args.collect:
        if args.files:
            input_file, output_file = args.files
            data_collection.data_collection_api(input_file, output_file)
            return
        else:
            data_collection.data_collection_api(APP_CONFIG['vulnerability dataset'], APP_CONFIG['dataset'])
            return
    
    # Data Process
    if args.process:
        if args.files:
            input_file, output_file = args.files
            data_process.data_process_api(input_file, output_file)
            return
        elif args.cve:
            data_process.data_process_api(APP_CONFIG['cve dataset'], APP_CONFIG['cve result'])
            return
        elif args.torchflow:
            data_process.data_process_api(APP_CONFIG['pytorch tensorflow dataset'], APP_CONFIG['pytorch tensorflow result'])
            return
        else:
            data_process.data_process_api(APP_CONFIG['dataset'], APP_CONFIG['result'])
            return

# main
if __name__ == "__main__":
    main()