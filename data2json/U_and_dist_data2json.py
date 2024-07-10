import pickle
import numpy as np
from datetime import datetime
import sys
import re
import glob
import os
import json
from pathlib import Path

#this script extracts effective data for U, L, y0,z0,y1


if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit()

funcName=sys.argv[1]
rowName=sys.argv[2]

TFolderRoot="../dataAll/"+funcName+"/"+rowName+"/"

obs_dist="dist"
obs_U="U"
#search directory
TVals=[]
TFileNames=[]
TStrings=[]
for TFile in glob.glob(TFolderRoot+"/T*"):
    # print(TFile)
    matchT=re.search(r"T([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)",TFile)
    if matchT:
        TFileNames.append(TFile)
        TVals.append(float(matchT.group(1)))
        TStrings.append("T"+matchT.group(1))
#sort T values
sortedInds=np.argsort(TVals)
sortedTVals=[TVals[ind] for ind in sortedInds]
sortedTFiles=[TFileNames[ind] for ind in sortedInds]
sortedTStrings=[TStrings[ind] for ind in sortedInds]

def parseSummary(oneTFolder,obs_name):
    """

    :param oneTFolder:
    :param obs_name:
    :return:
    """
    startingFileInd=-1
    startingVecPosition=-1
    lag=-1
    smrFile=oneTFolder+"/summary_"+obs_name+"/summaryFile_"+obs_name+".txt"
    summaryFileExists=os.path.isfile(smrFile)
    if summaryFileExists==False:
        return startingFileInd,startingVecPosition,-1
    # eq=False
    with open(smrFile,"r") as fptr:
        lines=fptr.readlines()
    for oneLine in lines:
        # #match equilibrium
        # matchEq=re.search(r"equilibrium",oneLine)
        # if matchEq:
        #     eq=True

        #match startingFileInd
        matchStartingFileInd=re.search(r"startingFileInd=(\d+)",oneLine)
        if matchStartingFileInd:
            startingFileInd=int(matchStartingFileInd.group(1))
        #match startingVecPosition
        matchStartingVecPosition=re.search(r"startingVecPosition=(\d+)",oneLine)
        if matchStartingVecPosition:
            startingVecPosition=int(matchStartingVecPosition.group(1))
        #match lag
        matchLag=re.search(r"lag=(\d+)",oneLine)
        if matchLag:
            lag=int(matchLag.group(1))

    return startingFileInd, startingVecPosition,lag

def sort_data_files_by_lpEnd(oneTFolder,obs_name):
    """

    :param oneTFolder: Txxx
    :return: pkl data files sorted by loopEnd
    """
    dataFolderName=oneTFolder+"/data_files/"+obs_name+"_AllPickle/"
    # print(dataFolderName)
    dataFilesAll=[]
    loopEndAll=[]

    for oneDataFile in glob.glob(dataFolderName+"/*.txt"):
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"loopEnd(\d+)",oneDataFile)
        if matchEnd:
            loopEndAll.append(int(matchEnd.group(1)))

    endInds=np.argsort(loopEndAll)
    # loopStartSorted=[loopStartAll[i] for i in startInds]
    sortedDataFiles=[dataFilesAll[i] for i in endInds]

    return sortedDataFiles

def dist_data2jsonForOneT(oneTFolder,oneTStr,startingFileInd,startingVecPosition,lag):
    """

    :param oneTFolder:
    :param oneTStr:
    :param startingFileInd:
    :param startingVecPosition:
    :return:
    """
    TRoot=oneTFolder
    sortedDataFilesToRead=sort_data_files_by_lpEnd(TRoot,obs_dist)
    # print("ind="+str(startingFileInd))
    # print("startingVecPosition="+str(startingVecPosition))
    startingFileName=sortedDataFilesToRead[startingFileInd]
    #read starting data file
    with open(startingFileName,"r") as fptr:
        content=fptr.read()
        # vec=np.array(pickle.load(fptr))
        vec=np.array([float(num.strip()) for num in content.split(',')])
        vecTruncated=vec[startingVecPosition*4:]
    #read the rest of the data files
    for inFile in sortedDataFilesToRead[(startingFileInd+1):]:
        with open(inFile,"r") as fptr:
            inContent=fptr.read()
            # inVec=np.array(pickle.load(fptr))
            inVec=np.array([float(num.strip()) for num in inContent.split(',')])
            vecTruncated=np.r_[vecTruncated,inVec]

    configNum=int(len(vecTruncated)/4)#number of [L,y0,z0,y1]
    # print(len(vecTruncated))
    LVec=[vecTruncated[4*j+0] for j in range(0,configNum)]
    # # print(len(LVec))
    y0Vec=[vecTruncated[4*j+1] for j in range(0,configNum)]

    z0Vec=[vecTruncated[4*j+2] for j in range(0,configNum)]

    y1Vec=[vecTruncated[4*j+3] for j in range(0,configNum)]

    LVecSelected=LVec[::lag]
    y0VecSelected=y0Vec[::lag]
    z0VecSelected=z0Vec[::lag]
    y1VecSelected=y1Vec[::lag]
    outJsonDataRoot=TFolderRoot+"/jsonOutAll/"
    outJsonFolder=outJsonDataRoot+"/"+oneTStr+"/jsonData/json"+obs_dist+"/"
    Path(outJsonFolder).mkdir(parents=True, exist_ok=True)
    outJsonFile=outJsonFolder+"/"+obs_dist+"Data.json"
    dataOut={
        "L":list(LVecSelected),
        "y0":list(y0VecSelected),
        "z0":list(z0VecSelected),
        "y1":list(y1VecSelected)
    }
    with open(outJsonFile,"w+") as fptr:
        json.dump(dataOut,fptr,indent=4)

def U_data2jsonForOneT(oneTFolder,oneTStr,startingFileInd,startingVecPosition,lag):
    """

    :param oneTFolder:
    :param oneTStr:
    :param startingFileInd:
    :param startingVecPosition:
    :param lag:
    :return:
    """
    TRoot=oneTFolder
    sortedDataFilesToRead=sort_data_files_by_lpEnd(TRoot,obs_U)
    startingFileName=sortedDataFilesToRead[startingFileInd]
    with open(startingFileName,"r") as fptr:
        content=fptr.read()
        # vec=np.array(pickle.load(fptr))
        vec=np.array([float(num.strip()) for num in content.split(',')])
        vecTruncated=vec[startingVecPosition:]
    #read the rest of the data files
    for inFile in sortedDataFilesToRead[(startingFileInd+1):]:
        with open(inFile,"r") as fptr:
            # inVec=np.array(pickle.load(fptr))
            inContent=fptr.read()
            inVec=np.array([float(num.strip()) for num in inContent.split(',')])
            vecTruncated=np.r_[vecTruncated,inVec]
    # configNum=int(len(vecTruncated))#number of U
    UVec=vecTruncated
    UVecSelected=UVec[::lag]
    outJsonDataRoot=TFolderRoot+"/jsonOutAll/"
    outJsonFolder=outJsonDataRoot+"/"+oneTStr+"/jsonData/json"+obs_U+"/"
    Path(outJsonFolder).mkdir(parents=True, exist_ok=True)
    outJsonFile=outJsonFolder+"/"+obs_U+"Data.json"
    dataOut={
        "U":list(UVecSelected)
    }
    with open(outJsonFile,"w+") as fptr:
        json.dump(dataOut,fptr,indent=4)
# oneTStr=sortedTStrings[0]
# oneTFolder=sortedTFiles[0]
# flIndTmp,vecIndTmp,lagTmp=parseSummary(oneTFolder,obs)
# data2jsonForOneT(oneTFolder,oneTStr,obs,flIndTmp,vecIndTmp,lagTmp)
for k in range(0,len(sortedTFiles)):
    tStart=datetime.now()
    oneTFolder=sortedTFiles[k]
    oneTStr=sortedTStrings[k]


    dist_startingfileIndTmp,dist_startingVecIndTmp,dist_lagTmp=parseSummary(oneTFolder,obs_dist)
    if dist_startingfileIndTmp<0:
        print("summary file does not exist for "+oneTStr+" "+obs_dist)
        continue

    dist_data2jsonForOneT(oneTFolder,oneTStr,dist_startingfileIndTmp,dist_startingVecIndTmp,dist_lagTmp)

    U_startingfileIndTmp,U_startingVecIndTmp,U_lagTmp=parseSummary(oneTFolder,obs_U)
    if U_startingfileIndTmp<0:
        print("summary file does not exist for "+oneTStr+" "+obs_U)
        continue
    U_data2jsonForOneT(oneTFolder,oneTStr,U_startingfileIndTmp,U_startingVecIndTmp,U_lagTmp)

    tEnd=datetime.now()
    print("processed T="+str(sortedTVals[k])+": ",tEnd-tStart)
