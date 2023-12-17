# Code Ownership in Open-Source AI Software Security
## 1 Overview

This repository offers tools for evaluating code ownership and computing time and release metrics. These tools and methodologies are directly inspired by the experimental findings and outcomes detailed in the paper. For an in-depth understanding of the theoretical background and practical applications, refer to the paper [Code Ownership in Open-Source AI Software Security](Code_Ownership_in_Open_Source_AI_Software_Security__RAIE_2024_.pdf).

## 2 Prerequisite

### 2.1 External Libraries

The tool has been created using Python and utilizes GitPython for repository analysis and pandas for data computations. Ensure the installation of these libraries prior to use.

* [Python 3.10.5 or above](https://www.python.org/)
* [GitPython](https://gitpython.readthedocs.io/en/stable/)
* [Pandas](https://pandas.pydata.org/)

### 2.2 RESTful API settings

#### GitHub

To authenticate with the GitHub API, it's necessary to obtain a [Personal Access Token](https://github.com/settings/tokens). This is essential for the tool to perform operations such as retrieving details of remote pull requests and commits. For information regarding the rate limits, consult the [GitHub Official Documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28).

Replace the token in the file [github_api.py](/metric_calculation/utils/github_api.py) located in the `utils` folder. For example:

    """
    TOKEN used for Github
    """
    TOKEN = "" # replace with ur Github Token
    HEADERS = {
        'Authorization': f'token {TOKEN}',
        'User-Agent': 'Code Ownership'
    }

#### NVD

It's necessary to obtain an [NVD API Token](https://nvd.nist.gov/developers/request-an-api-key) for accessing the CVE Severity information from the National Vulnerability Database. For comprehensive details on API usage, consult the [Vulnerabilities Documentation](https://nvd.nist.gov/developers/vulnerabilities).

Incorporate this token into the [nvd_api.py](/metric_calculation/utils/nvd_api.py) file located in the `utils` folder, as follows:

    """
    NVD API key
    """
    API_KEY = "" # replace with ur NVD Token
    HEADERS = {"apiKey": API_KEY}

## 3 Tool Interface

The metric computation process is divided into two distinct command-line interfaces. This division is intended to simplify usage and to distinctly separate the analysis of bias between GitHub repositories and source code files.

### 3.1 Usage I (for Individual Files)

The options for the interfaces are:

    PS Code-Ownership\metric_calculation\file_interface> python app.py -h
    usage: app.py [-h] [--cve] [--torchflow] [--files Src Dst] [-c] [-p]

    Source Code Examination Interface

    options:
    -h, --help       show this help message and exit
    --cve            Use default CVE dataset
    --torchflow      Use default Pytorch/Tensorflow dataset
    --files Src Dst  Specify input and output csv file destination
    -c, --collect    Collect data from the source code info dataset
    -p, --process    Process the dataset (use default dataset without other flags specified)

#### 3.1.1 Vulnerability Information Collection

Within the `file_interface` directory, the interface facilitates the input of multiple source code files along with specific details in a single Excel (xlsx) file. This input file must include the following mandatory fields: `Framework` (indicating the source of the repository) and `Patch URLs` (pointing to the source of vulnerability information as pull requests/commits). An optional field is `CVE ID`, which provides additional CVE information. An example input file can be found at [/metric_calculation/file_interface/data/example_vulnerability.xlsx](/metric_calculation/file_interface/data/example_vulnerability.xlsx).

When using the command-line interface, it is necessary to specify both the input xlsx file and the output dataset file for subsequent metric calculations. This is achieved using the `-c` or `--collect` flag:

    PS \metric_calculation\file_interface> python app.py --files  data/example_vulnerability.xlsx data/example_dataset.csv -c


#### 3.1.2 Metric Calculation

Following the provision of vulnerability information, the tool will transform the raw data into an operational dataset. In the command line interface, input the dataset processed as described in section 3.1.1, and designate the destination for the metric calculation output, which should be in CSV file format. An example input CSV file is available at [/metric_calculation/file_interface/data/example_dataset.csv](/metric_calculation/file_interface/data/example_dataset.csv).

Within the command line interface, you should specify the input CSV file from section 3.1.1 and the output CSV result file using the `-p` or `--process` flag:

    PS \metric_calculation\file_interface> python app.py --files  data/example_dataset.csv data/example_result.csv -p

### 3.2 Usage II (for Repository)

The options for the interface are:

    PS Code-Ownership\metric_calculation\repo_interface> python app.py -h
    usage: app.py [-h] [--url URL] [--dst Dst] [-p]

    GitHub Repository Examination Interface

    options:
    -h, --help     show this help message and exit
    --url URL      Specify the REPO URL
    --dst Dst      Specify the result destination
    -p, --process  Process the default URLs

In the `repo_interface` directory, the interface enables users to input a Git repository URL, whether it's a local or remote repository. The program will then analyze the code ownership details across all the files within the repository, spanning from the initial day of the repository's creation to the day the program is executed.

When using the command line interface, it is necessary to specify the repository URL for analysis and also designate the output CSV result file. The usage would be as follows:

    PS \metric_calculation\repo_interface>python app.py --url "https://github.com/tensorflow/tensorflow" --dst result.csv -p

### 3.3 Result Output

The results of the metric calculations are compiled into a single CSV file. This file encompasses a range of information, including metrics like `Ownership`, `Num of Minor`, `Time Stage Aged`, and more. For reference, an example of the result file can be found at [/metric_calculation/repo_interface/data/example_results.csv](/metric_calculation/repo_interface/data/example_results.csv). These results provide a detailed overview of code ownership across the repository or individual source code files. This comprehensive analysis assists developers in making informed decisions for subsequent operations and effective security management.

## 4 Note

The tool is currently in ongoing development to enhance its performance and user interaction. Should you encounter any issues or have suggestions for improvement, we welcome your feedback. Please feel free to contact the team via jwen8784@uni.sydney.edu.au.



