import numpy as np
import glob
import sys
import re
import matplotlib.pyplot as plt
from datetime import datetime
import json
#this script computes thermal expansion

argErrCode=2

if (len(sys.argv)!=3):
    print("wrong number of arguments")
    exit(argErrCode)

funcName=sys.argv[1]
rowName=sys.argv[2]

TFolderRoot="../dataAll/"+funcName+"/"+rowName+"/jsonOutAll/"
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

def compute_alpha(oneTFile):
    """

    :param oneTFile: corresponds to one temperature
    :return: one alpha value
    """
    matchT=re.search(r"T(\d+(\.\d+)?)",oneTFile)
    TVal=float(matchT.group(1))

    distFilePath=oneTFile+"/jsonData/jsondist/distData.json"

    with open(distFilePath,"r") as fptr:
        distJsonData=json.load(fptr)
    LVec=np.array(distJsonData["L"])
    UFilePath=oneTFile+"/jsonData/jsonU/UData.json"
    with open (UFilePath,"r") as fptr:
        UData=json.load(fptr)

    UVec=np.array(UData["U"])
    LUProd=LVec*UVec

    LUMean=np.mean(LUProd)

    LMean=np.mean(LVec)

    UMean=np.mean(UVec)

    alphaVal=1/(TVal**2*LMean)*(LUMean-LMean*UMean)

    return alphaVal


tStart=datetime.now()

alphaAll=[]

for oneTFile in sortedTFiles:
    alphaTmp=compute_alpha(oneTFile)
    alphaAll.append(alphaTmp)
tEnd=datetime.now()

alphaAll=np.array(alphaAll)
print("alpha time: ",tEnd-tStart)
sortedTVals=np.array(sortedTVals)
TInds=np.where(sortedTVals<100)
TToPlt=sortedTVals[TInds]
interpolatedTVals=np.linspace(np.min(TToPlt)*0.9,np.max(TToPlt)*1.1,30)
plt.figure()

plt.plot(interpolatedTVals,[0]*len(interpolatedTVals),color="black",label="theory")
plt.scatter(TToPlt,alphaAll[TInds],color="red",label="mc")
plt.title("Thermal expansion")
plt.xlabel("$T$")
plt.ylabel("$\\alpha$")
plt.ylim((-0.025,0.025))
plt.legend(loc="best")
plt.savefig(TFolderRoot+"/alpha.png")
plt.close()






