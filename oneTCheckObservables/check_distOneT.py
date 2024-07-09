import pickle
import numpy as np
from datetime import datetime
import statsmodels.api as sm
import sys
import re
import warnings
from scipy.stats import ks_2samp
import glob
from pathlib import Path
import os
import json
#This script checks if  L, y0,z0,y1 values reach equilibrium and writes summary file of dist

argErrCode=1

if (len(sys.argv)!=2):
    print("wrong number of arguments")
    exit(argErrCode)

jsonFromSummaryLast=json.loads(sys.argv[1])

dist_Dir=jsonFromSummaryLast["dist_Dir"]

summaryFile=dist_Dir+"/summary_dist/summaryFile_dist.txt"

def sort_data_files_by_lpEnd(oneDir):
    dataFilesAll=[]
    loopEndAll=[]
    for oneDataFile in glob.glob(oneDir+"/*.pkl"):
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"loopEnd(\d+)",oneDataFile)
    endInds=np.argsort(loopEndAll)
    sortedDataFiles=[dataFilesAll[i] for i in endInds]
    return sortedDataFiles



def parseSummary(oneDir):
    startingFileInd=-1
    startingVecPosition=-1

    summaryFileExists=os.path.isfile(summaryFile)
    if summaryFileExists==False:
        return startingFileInd,startingVecPosition


    with open(summaryFile,"r") as fptr:
        lines=fptr.readlines()
    for oneLine in lines:
        #match startingFileInd
        matchStartingFileInd=re.search(r"startingFileInd=(\d+)",oneLine)
        if matchStartingFileInd:
            startingFileInd=int(matchStartingFileInd.group(1))

        #match startingVecPosition
        matchStartingVecPosition=re.search(r"startingVecPosition=(\d+)",oneLine)
        if matchStartingVecPosition:
            startingVecPosition=int(matchStartingVecPosition.group(1))


    return startingFileInd, startingVecPosition


def checkDataFilesForOneT(oneDir):
    TRoot=oneDir
    sortedDataFilesToRead=sort_data_files_by_lpEnd(TRoot)
    if len(sortedDataFilesToRead)==0:
        print("no data.")
        exit(0)

    parsedStartingFileInd,parsedStartingVecPosition=parseSummary(oneDir)

    if parsedStartingFileInd>0:
        startingFileInd=parsedStartingFileInd
    else:
        startingFileInd=int(len(sortedDataFilesToRead)*1/2)#we guess that the equilibrium starts within this data file


    startingFileName=sortedDataFilesToRead[startingFileInd]
    startingVecPosition=0

    #read starting data file
    with open(startingFileName,"rb") as fptr:
        vec=np.array(pickle.load(fptr))
        lengthTmp=len(vec)
        if parsedStartingVecPosition>0:
            startingVecPosition=parsedStartingVecPosition
        else:
            startingVecPosition=int(lengthTmp/2)#we guess that the equilibrium starts at this position
        vecTruncated=vec[startingVecPosition:]


    for inFile in sortedDataFilesToRead[(startingFileInd+1):]:
        with open(inFile,"rb") as fptr:
            inVec=np.array(pickle.load(fptr))
            vecTruncated=np.r_[vecTruncated,inVec]

    #extract L, y0,z0,y1

    configNum=int(len(vecTruncated)/4)
    print(configNum)