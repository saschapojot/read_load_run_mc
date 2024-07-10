import sys
import glob
import re
import json
from decimal import Decimal
import pickle
import numpy as np

#this script loads previous data
numArgErr=4
if (len(sys.argv)!=3):
    print("wrong number of arguments.")
    exit(numArgErr)

jsonDataFromConf =json.loads(sys.argv[1])
jsonFromSummary=json.loads(sys.argv[2])

potential_function_name=jsonDataFromConf["potential_function_name"]
parameter_file_row=str(jsonDataFromConf["parameter_file_row"])
T_list_str = jsonDataFromConf['T']
T_list = [float(value) for value in T_list_str.split(',')]
def format_using_decimal(value):
    # Convert the float to a Decimal
    decimal_value = Decimal(value)
    # Remove trailing zeros and ensure fixed-point notation
    formatted_value = decimal_value.quantize(Decimal(1)) if decimal_value == decimal_value.to_integral() else decimal_value.normalize()
    return str(formatted_value)

TVal=format_using_decimal(T_list[0])
startingFileInd=jsonFromSummary["startingFileInd"]
startingVecPosition=jsonFromSummary["startingVecPosition"]
newMcStepNum=jsonFromSummary["newMcStepNum"]
distDataDir=jsonFromSummary["dist_Dir"]



#search and read dist files
#give arbitrary values to L, y0, z0, y1 without reading data
LInit=1
y0Init=2
z0Init=3
y1Init=4
loopLastFile=-1
#########################################
##search pkl files
# pklFileList=[]
# loopEndAll=[]
# # print(distDataDir)
# for file in glob.glob(distDataDir+"/*.pkl"):
#     pklFileList.append(file)
#     matchEnd=re.search(r"loopEnd(\d+)",file)
#     if matchEnd:
#         loopEndAll.append(int(matchEnd.group(1)))
###############################################
#############################################
#search txt files
txtFileList=[]
loopEndAll=[]
for file in glob.glob(distDataDir+"/*.txt"):
    txtFileList.append(file)
    matchEnd=re.search(r"loopEnd(\d+)",file)
    if matchEnd:
        loopEndAll.append(int(matchEnd.group(1)))

#############################################

# print(pklFileList)
#if no data found, return the arbitrary values
if len(txtFileList)==0:
    initDataJson={
        "L":LInit,
        "y0":y0Init,
        "z0":z0Init,
        "y1":y1Init,
        "loopLastFile":loopLastFile
    }

    print(json.dumps(initDataJson))
    exit(0)

#if found pkl data
sortedEndInds=np.argsort(loopEndAll)
sortedLoopEnd=[loopEndAll[ind] for ind in sortedEndInds]
sortedPklFileNames=[txtFileList[ind] for ind in sortedEndInds]
loopLastFile=sortedLoopEnd[-1]



lastFileName=sortedPklFileNames[-1]
with open(lastFileName,"r") as fptr:
    # vec=pickle.load(fptr)
    content = fptr.read()
    vec=np.array([float(num.strip()) for num in content.split(',')])

LInit,y0Init,z0Init,y1Init=vec[-4:]

initDataJson={
    "L":LInit,
    "y0":y0Init,
    "z0":z0Init,
    "y1":y1Init,
    "loopLastFile":loopLastFile
}

print(json.dumps(initDataJson))
exit(0)