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
#This script checks if U, L, y0,z0,y1 values reach equilibrium and writes summary file of dist

argErrCode=2
sameErrCode=3
if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit(argErrCode)

jsonFromSummaryLast=json.loads(sys.argv[1])
jsonDataFromConf=json.loads(sys.argv[2])
dataDir=jsonFromSummaryLast["dataDir"]
dist_Dir=jsonFromSummaryLast["dist_Dir"]
# print("dist_Dir="+dist_Dir)
U_Dir=jsonFromSummaryLast["U_Dir"]
effective_data_num_required=int(jsonDataFromConf["effective_data_num_required"])
# print(effective_data_num_required)
# print(dist_Dir)
summaryDist=dataDir+"/summary_dist/"
summaryU=dataDir+"/summary_U/"
# print(summaryDist)
Path(summaryDist).mkdir(exist_ok=True,parents=True)
Path(summaryU).mkdir(exist_ok=True,parents=True)
summary_distFile=summaryDist+"/summaryFile_dist.txt"
summary_UFile=summaryU+"/summaryFile_U.txt"

def sort_data_files_by_lpEnd(oneDir):
    dataFilesAll=[]
    loopEndAll=[]
    for oneDataFile in glob.glob(oneDir+"/*.txt"):
        # print(oneDataFile)
        dataFilesAll.append(oneDataFile)
        matchEnd=re.search(r"loopEnd(\d+)",oneDataFile)
        if matchEnd:
            indTmp=int(matchEnd.group(1))
            loopEndAll.append(indTmp)
    endInds=np.argsort(loopEndAll)
    sortedDataFiles=[dataFilesAll[i] for i in endInds]
    return sortedDataFiles

# print(sort_data_files_by_lpEnd(dist_Dir))

def parseSummaryDist():
    startingFileInd=-1
    startingVecPosition=-1

    summaryFileExists=os.path.isfile(summary_distFile)
    if summaryFileExists==False:
        return startingFileInd,startingVecPosition


    with open(summary_distFile,"r") as fptr:
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

def parseSummaryU():
    """

    :return:
    """
    startingFileInd=-1
    startingVecPosition=-1

    summaryFileExists=os.path.isfile(summary_UFile)
    if summaryFileExists==False:
        return startingFileInd,startingVecPosition

    with open(summary_distFile,"r") as fptr:
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

def checkDataFilesForOneT(dist_pkl_dir, U_pkl_dir):
    """

    :param dist_pkl_dir:
    :param U_pkl_dir:
    :return:
    """



    dist_sortedDataFilesToRead=sort_data_files_by_lpEnd(dist_pkl_dir)
    # print(dist_sortedDataFilesToRead)
    U_sortedDataFilesToRead=sort_data_files_by_lpEnd(U_pkl_dir)
    if len(dist_sortedDataFilesToRead)==0:
        print("no data for dist.")
        exit(0)
    if len(U_sortedDataFilesToRead)==0:
        print("no data for U.")
        exit(0)

    dist_parsedStartingFileInd,dist_parsedStartingVecPosition=parseSummaryDist()
    U_parsedStartingFileInd,U_parsedStartingVecPosition=parseSummaryU()

    if dist_parsedStartingFileInd>0 and U_parsedStartingFileInd>0:
        startingFileInd=np.max([dist_parsedStartingFileInd,U_parsedStartingFileInd])
    else:
        startingFileInd=int(len(dist_sortedDataFilesToRead)*1/2)#we guess that the equilibrium starts within this data file


    dist_startingFileName=dist_sortedDataFilesToRead[startingFileInd]
    U_startingFileName=U_sortedDataFilesToRead[startingFileInd]

    dist_startingVecPosition=0
    U_startingVecPosition=0

    # #read starting dist data file
    with open(dist_startingFileName,"r") as fptr:
        dist_content = fptr.read()
        dist_vec=np.array([float(num.strip()) for num in dist_content.split(',')])

        if dist_parsedStartingFileInd>0:
            dist_startingVecPosition=dist_parsedStartingVecPosition
        else:
            dist_configNumInFirstFile=int(len(dist_vec)/4)
            # print(len(vec))
            # print(configNumInFirstFile)
            dist_startingVecPosition=int(dist_configNumInFirstFile/2)#we guess that the equilibrium starts at this configuration

        # vecTruncated=vec[startingVecPosition*4:]#remember that every 4 numbers are L, y0, z0, y1

    with open(U_startingFileName,"r")as fptr:
        # U_vec=np.array(pickle.load(fptr))
        U_content=fptr.read()
        U_vec=np.array([float(num.strip()) for num in U_content.split(',')])

        U_lengthTmp=len(U_vec)
        if U_parsedStartingFileInd>0:
            U_startingVecPosition=U_parsedStartingVecPosition
        else:
            U_startingVecPosition=int(U_lengthTmp)/2

    startingVecPosition=int(np.max([dist_startingVecPosition,U_startingVecPosition]))

    dist_vecTruncated=dist_vec[startingVecPosition*4:]
    U_vecTruncated=U_vec[startingVecPosition:]
    #read the rest of dist.pkl files
    for dist_inFile in dist_sortedDataFilesToRead[(startingFileInd+1):]:
        with open(dist_inFile,"r") as fptr:
            # dist_inVec=np.array(pickle.load(fptr))
            dist_inContent=fptr.read()
            dist_inVec=np.array([float(num.strip()) for num in dist_inContent.split(',')])
            dist_vecTruncated=np.r_[dist_vecTruncated,dist_inVec]

    #read the rest of U.pkl files
    for U_inFile in U_sortedDataFilesToRead[(startingFileInd+1):]:
        with open(U_inFile,"r") as fptr:
            U_inContent=fptr.read()
            # U_inVec=np.array(pickle.load(fptr))
            U_inVec=np.array([float(num.strip()) for num in U_inContent.split(',')])
            U_vecTruncated=np.r_[U_vecTruncated,U_inVec]


    configNum=int(len(dist_vecTruncated)/4)#number of [L,y0,z0,y1]
    # print(configNum)
    # print(len(U_vecTruncated))
    #
    LVec=[dist_vecTruncated[4*j+0] for j in range(0,configNum)]
    # # print(len(LVec))
    y0Vec=[dist_vecTruncated[4*j+1] for j in range(0,configNum)]

    z0Vec=[dist_vecTruncated[4*j+2] for j in range(0,configNum)]

    y1Vec=[dist_vecTruncated[4*j+3] for j in range(0,configNum)]

    UVec=U_vecTruncated

    NLags=int(len(LVec)*3/4)

    eps=1e-3
    lagVal=-1
    same=False

    # #compute auto-correlations
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
    try:
        acfOfVecL=sm.tsa.acf(LVec,nlags=NLags)
    except Warning as w:
        same=True

    try:
        acfOfVecy0=sm.tsa.acf(y0Vec,nlags=NLags)
    except Warning as w:
        same=True

    try:
        acfOfVecz0=sm.tsa.acf(y0Vec,nlags=NLags)
    except Warning as w:
        same=True

    try:
        acfOfVecy1=sm.tsa.acf(y0Vec,nlags=NLags)
    except Warning as w:
        same=True

    try:
        acfOfVecU=sm.tsa.acf(UVec,nlags=NLags)
    except Warning as w:
        same=True
    #all values are the same, exit with err code
    if same==True:
        with open(summary_distFile,"w+") as fptr:
            msg="error: same\n"
            fptr.writelines(msg)

        with open(summary_UFile,"w+") as fptr:
            msg="error: same\n"
            fptr.writelines(msg)
        exit(sameErrCode)

    acfOfVecLAbs=np.abs(acfOfVecL)
    acfOfVecy0Abs=np.abs(acfOfVecy0)
    acfOfVecz0Abs=np.abs(acfOfVecz0)
    acfOfVecy1Abs=np.abs(acfOfVecy1)
    acfOfVecUAbs=np.abs(acfOfVecU)



    minAutcL=np.min(acfOfVecLAbs)
    minAutcy0=np.min(acfOfVecy0Abs)
    minAutcz0=np.min(acfOfVecz0Abs)
    minAutcy1=np.min(acfOfVecy1Abs)
    minAutcU=np.min(acfOfVecUAbs)

    # print(minAutcL)
    # print(minAutcy0)
    # print(minAutcz0)
    # print(minAutcy1)
    # print(minAutcU)

    if minAutcL<eps and minAutcy0< eps\
        and minAutcz0<eps and minAutcy1<eps and minAutcU<eps:

        lagL=np.where(acfOfVecLAbs<=eps)[0][0]
        lagy0=np.where(acfOfVecy0Abs<=eps)[0][0]
        lagz0=np.where(acfOfVecz0Abs<=eps)[0][0]
        lagy1=np.where(acfOfVecy1Abs<=eps)[0][0]
        lagU=np.where(acfOfVecUAbs<=eps)[0][0]

        lagVal=np.max([lagL,lagy0,lagz0,lagy1,lagU])
        # print(lagVal)


    # #     #select values by lagVal
        LVecSelected=LVec[::lagVal]
        y0VecSelected=y0Vec[::lagVal]
        z0VecSelected=z0Vec[::lagVal]
        y1VecSelected=y1Vec[::lagVal]
        UVecSelected=UVec[::lagVal]


        lengthTmp=len(LVecSelected)
        if lengthTmp%2==1:
            lengthTmp-=1
        lenPart=int(lengthTmp/2)
        # print(lenPart)
        LVecValsToCompute=LVecSelected[-lengthTmp:]
        y0VecValsToCompute=y0VecSelected[-lengthTmp:]
        z0VecValsToCompute=z0VecSelected[-lengthTmp:]
        y1VecValsToCompute=y1VecSelected[-lengthTmp:]
        UVecValsToCompute=UVecSelected[-lengthTmp:]


    #     # #test distributions

        #test L
        selectedLVecPart0=LVecValsToCompute[:lenPart]
        selectedLVecPart1=LVecValsToCompute[lenPart:]
        resultL=ks_2samp(selectedLVecPart0,selectedLVecPart1)

        #test y0
        selectedy0VecPart0=y0VecValsToCompute[:lenPart]
        selectedy0VecPart1=y0VecValsToCompute[lenPart:]
        resulty0=ks_2samp(selectedy0VecPart0,selectedy0VecPart1)


        #test z0
        selectedz0VecPart0=z0VecValsToCompute[:lenPart]
        selectedz0VecPart1=z0VecValsToCompute[lenPart:]
        resultz0=ks_2samp(selectedz0VecPart0,selectedz0VecPart1)


        #test y1
        selectedy1VecPart0=y1VecValsToCompute[:lenPart]
        selectedy1VecPart1=y1VecValsToCompute[lenPart:]
        resulty1=ks_2samp(selectedy1VecPart0,selectedy1VecPart1)

        #test U
        selectedUVecPart0=UVecValsToCompute[:lenPart]
        selectedUVecPart1=UVecValsToCompute[lenPart:]
        resultU=ks_2samp(selectedUVecPart0,selectedUVecPart1)



        numDataPoints=len(selectedLVecPart0)+len(selectedLVecPart1)
        pValsAll=np.array([resultL.pvalue,resulty0.pvalue,resultz0.pvalue,resulty1.pvalue,resultU.pvalue])
        # print(pValsAll)

        if np.min(pValsAll)>=eps and numDataPoints>=200:
            if numDataPoints>=effective_data_num_required:
                newDataPointNum=0
            else:
                newDataPointNum=effective_data_num_required-numDataPoints

            msg="equilibrium\n" \
                +"lag="+str(lagVal)+"\n" \
                +"numDataPoints="+str(numDataPoints)+"\n" \
                +"startingFileInd="+str(startingFileInd)+"\n" \
                +"startingVecPosition="+str(startingVecPosition)+"\n" \
                +"newDataPointNum="+str(newDataPointNum)+"\n"
            with open(summary_distFile,"w+") as fptr:
                fptr.writelines(msg)
            with open(summary_UFile,"w+") as fptr:
                fptr.writelines(msg)
            exit(0)

        continueMsg="continue\n"
        if np.min(pValsAll)<0.1:
            #not the same distribution
            continueMsg+="p value: "+str(np.min(pValsAll))+"\n"
        if numDataPoints<200:
            #not enough data number
            continueMsg+="numDataPoints="+str(numDataPoints)+" too low\n"
        with open(summary_distFile,"w+") as fptr:
            fptr.writelines(continueMsg)
        with open(summary_UFile,"w+") as fptr:
            fptr.writelines(continueMsg)
        exit(0)

    else:
        highMsg="high correlation"
        with open(summary_distFile,"w+") as fptr:
            fptr.writelines(highMsg)
        with open(summary_UFile,"w+") as fptr:
            fptr.writelines(highMsg)
        exit(0)

checkDataFilesForOneT(dist_Dir,U_Dir)