import os, re, sys, git, subprocess, time
from datetime import datetime


# metric class
class Component:
    def __init__(self, name, componentType):
        # basic
        self.name = name
        self.componentType = componentType # file or folder (not folder perhaps, locality, just a collection of commit/defects)
        # code ownership
        self.ownership = 0 # ownership of the component
        self.contribute = {} # dict of contributors with their contributions
        self.contributorNum = 0
        self.minorNum5 = 0 # number of minor contributors, 5%
        self.minorPer5 = 0 # percentage of the minor contributors, 5%
        self.minorContriAvg5 = 0 # average of the minor contributors' contribution, 5%
        self.minorNum10 = 0 # number of minor contributors, 10%
        self.minorPer10 = 0 # percentage of the minor contributors, 10%
        self.minorContriAvg10 = 0 # average of the minor contributors' contribution, 10%
        self.minorNum20 = 0 # number of minor contributors, 20%
        self.minorPer20 = 0 # percentage of the minor contributors, 20%
        self.minorContriAvg20 = 0 # average of the minor contributors' contribution, 20%
        self.minorNum50 = 0 # number of minor contributors, 50%
        self.minorPer50 = 0 # percentage of the minor contributors, 50%
        self.minorContriAvg50 = 0 # average of the minor contributors' contribution, 50%
        # time
        self.time = None # days difference
        self.release = None # release statistic at collection (major, minor, pre_release, patch, alpha_beta)
        self.timeType = None # Five stages of the time
        self.ossStage = None # Six stages of the OSS project
        # license
        self.licenseInfo = None
        self.licenseType = None
        # "classical" process metric
        self.total_added = 0
        self.total_deleted = 0
        self.filesize = 0
        
    # add contributor info
    def addContribute(self, contributor, contribution):
        self.contribute[contributor] = self.contribute.get(contributor, 0) + contribution 
        # the definition of contribution, based on the commit amount or just for each commit (paper)

    # calculate the ownership info
    def calculateOwnership(self):
        sum_of_contri = sum(self.contribute.values())
        max_of_contri = max(self.contribute.values())
        
        self.ownership = max_of_contri / sum_of_contri # ownership
        self.contributorNum = len(self.contribute)
        
        self.minorNum5, self.minorPer5, self.minorContriAvg5 = self.calculateOwnershipThreshold(0.05, sum_of_contri) # 5%
        self.minorNum10, self.minorPer10, self.minorContriAvg10 = self.calculateOwnershipThreshold(0.10, sum_of_contri) # 10%
        self.minorNum20, self.minorPer20, self.minorContriAvg20 = self.calculateOwnershipThreshold(0.20, sum_of_contri) # 20%
        self.minorNum50, self.minorPer50, self.minorContriAvg50 = self.calculateOwnershipThreshold(0.50, sum_of_contri) # 50%
        
        return
    
    def calculateOwnershipThreshold(self, threshold, sum_of_contri):
        minorNum = 0
        minorPer = 0
        minorContriAvg = 0
        for key, value in self.contribute.items():
            contri = value / sum_of_contri
            if contri <= threshold:
                minorNum += 1
                minorContriAvg += contri
        
        minorPer = minorNum / len(self.contribute)
        if minorNum > 0:
            minorContriAvg /= minorNum
        return minorNum, minorPer, minorContriAvg
    
    def setTime(self, time_info, release_info, timeType, ossStage):
        self.time = time_info
        self.release = release_info
        self.timeType = timeType
        self.ossStage = ossStage
    
    def setLicense(self, licenseInfo, licenseType):
        self.licenseInfo = licenseInfo
        self.licenseType = licenseType
    
    def setClassic(self, total_added, total_deleted, filesize):
        self.total_added = total_added
        self.total_deleted = total_deleted
        self.filesize = filesize


def inComponents(components, name):
    for component in components:
        if component.name == name:
            return component
    return None


# calculate the time info
def calculateTime(time, release, log_time, log_release):
    # five stages of time
    timeType = None
    if time in range(0, 7):
        timeType = "t1" # 0 ~ 7 days
    elif time in range(7, 90):
        timeType = "t2" # 7 days ~ 3 months
    elif time in range(90, 270):
        timeType = "t3" # 3 months ~ 9 months
    elif time in range(270, 1096):
        timeType = "t4" # 2 ~ 3 years
    elif time > 1097:
        timeType = "t5"
    
    # release combined (success/tragedy)
    ossStage = None
    if sum(release) >= 1:
        ossStage = "SI"
    if sum(release) == 0 and time >= 365:
        ossStage = "TI"
    if sum(release) == 0 and time < 365:
        ossStage = "II"
    
    release_dates = list(log_release.values())
    latest_time = log_time.splitlines()[-1]
    parts = latest_time.split()
    latest_time = ' '.join(parts[1:]).replace("'", "")
    
    if sum(release) in range(1, 3) and timeDifference(latest_time, release_dates[0]) < 365:
        ossStage = "IG"
    if sum(release) == 3 and timeDifference(release_dates[0], release_dates[2]) < 180:
        ossStage = "IG"
        
    if sum(release) >= 3 and timeDifference(release_dates[0], release_dates[2]) > 180:
        ossStage = "SG"
    if sum(release) in range(1, 3) and timeDifference(latest_time, release_dates[0]) >= 365:
        ossStage = "TG"
    
    return timeType, ossStage


def timeDifference(t1, t2):
    # Convert date strings to datetime objects
    date_format = "%Y-%m-%d %H:%M:%S %z"
    datetime1 = datetime.strptime(t1, date_format)
    datetime2 = datetime.strptime(t2, date_format)

    # Calculate the difference in days
    time_difference = datetime1 - datetime2
    days_difference = time_difference.days
    
    return days_difference


def checkLicenseType(licenseInfo):
    copylefts = ["GNU GENERAL PUBLIC", "Eclipse Public", 
                    "GNU AFFERO GENERAL PUBLIC", "GNU LESSER GENERAL PUBLIC", "Mozilla Public"]
    permissives = ["Apache", "MIT", "BSD 2-Clause", "BSD 3-Clause", 
                    "Boost Software", "Eclipse Public", "Unlicense"]
    
    licenseType = None
    if licenseInfo in copylefts:
        licenseType = "copyleft"
    elif licenseInfo in permissives:
        licenseType = "permissive"
    return licenseType