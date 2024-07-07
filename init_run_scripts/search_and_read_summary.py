import re
from decimal import Decimal
import json
import sys
from pathlib import Path
import os
import shutil
from distutils.util import strtobool

#this script initializes the parameters for mc computation by reading summary file
invalidValueErrCode=1
mcErrCode=2
pathErrCode=3
numArgErr=4
if (len(sys.argv)!=2):
    print("wrong number of arguments.")
    exit(numArgErr)

jsonData=json.loads(sys.argv[1])

#read json
T_list_str = jsonData['T']
T_list = [float(value) for value in T_list_str.split(',')]
#check if T values are positive numbers
for val in T_list:
    if val<=0:
        print("invalid temperature: "+str(val))
        exit(invalidValueErrCode)
def format_using_decimal(value):
    # Convert the float to a Decimal
    decimal_value = Decimal(value)
    # Remove trailing zeros and ensure fixed-point notation
    formatted_value = decimal_value.quantize(Decimal(1)) if decimal_value == decimal_value.to_integral() else decimal_value.normalize()
    return str(formatted_value)

TVal=format_using_decimal(T_list[0])
# print(jsonData)
erase_data_if_exist=bool(strtobool(jsonData["erase_data_if_exist"]))
# print("erase_data_if_exist="+str(erase_data_if_exist))
search_and_read_summary_file=bool(strtobool(jsonData["search_and_read_summary_file"]))
potential_function_name=jsonData["potential_function_name"]
parameter_file=jsonData["parameter_file"]
parameter_file_row=int(jsonData["parameter_file_row"])
effective_data_num_required=int(jsonData["effective_data_num_required"])
loop_to_write=int(jsonData["loop_to_write"])
default_flush_num=int(jsonData["default_flush_num"])
#data folder
dataDir="./dataAll/"+potential_function_name+"/row"+str(parameter_file_row)+"/T"+str(TVal)+"/"



# Path(dataDir).mkdir(exist_ok=True,parents=True)
if erase_data_if_exist==True:
    if os.path.isdir(dataDir):
        try:
            shutil.rmtree(dataDir)
            print(f'Directory {dataDir} and all its contents have been removed successfully')
        except OSError as e:
            print(f'Error: {dataDir} : {e.strerror}')
            exit(pathErrCode)

#create dataDir if not exists
Path(dataDir).mkdir(exist_ok=True, parents=True)


#parameters to guide mc computation
lag=-1
startingFileInd=-1
startingVecPosition=-1
newDataPointNum=-1

newMcStepNum=loop_to_write*default_flush_num

# usingParamsInSummary=False
# if search_and_read_summary_file==True:
#     usingParamsInSummary=True





#if observable_name not found, return -1,-1, loop_to_write*default_flush_num, then exit with code 0
if "observable_name" not in jsonData:
    outDict={
        "startingFileInd":startingFileInd,
        "startingVecPosition":startingVecPosition,
        "newMcStepNum":newMcStepNum,
        "newDataPointNum":newDataPointNum

    }
    print(json.dumps(outDict))
    exit(0)

obs_name=jsonData["observable_name"]
# print("obs_name="+obs_name)
summaryFileName=dataDir+"/summary_"+obs_name+"/summaryFile_"+obs_name+".txt"

summaryFileExists= os.path.isfile(summaryFileName)


#if summary file does not exist, return -1,-1, loop_to_write*default_flush_num, then exit with code 0

if summaryFileExists==False:
    outDict={
        "startingFileInd":startingFileInd,
        "startingVecPosition":startingVecPosition,
        "newMcStepNum":newMcStepNum,
        "newDataPointNum":newDataPointNum

    }
    print(json.dumps(outDict))
    # print("startingFileInd="+str(startingFileInd)+", startingVecPosition="+str(startingVecPosition)+", newMcStepNum="+str(newMcStepNum)+", newDataPointNum="+str(newDataPointNum))
    exit(0)

#parse summary file

with open(summaryFileName,"r") as fptr:
    linesInSummaryFile= fptr.readlines()


for oneLine in linesInSummaryFile:
    matchErr=re.search(r"error",oneLine)
    #if "error" is matched
    if matchErr:
        print("error in previous computation, please re-run.")
        exit(mcErrCode)

    #if "continue" is matched
    matchContinue=re.search(r"continue",oneLine)
    if matchContinue:
        outDict={
            "startingFileInd":startingFileInd,
            "startingVecPosition":startingVecPosition,
            "newMcStepNum":newMcStepNum,
            "newDataPointNum":newDataPointNum

        }
        print(json.dumps(outDict))
        # print("startingFileInd="+str(startingFileInd)+", startingVecPosition="+str(startingVecPosition)+", newMcStepNum="+str(newMcStepNum)+", newDataPointNum="+str(newDataPointNum))
        exit(0)

    #if "high" is matched
    matchHigh=re.search(r"high",oneLine)
    if matchHigh:
        outDict={
            "startingFileInd":startingFileInd,
            "startingVecPosition":startingVecPosition,
            "newMcStepNum":newMcStepNum,
            "newDataPointNum":newDataPointNum

        }
        print(json.dumps(outDict))
        # print("startingFileInd="+str(startingFileInd)+", startingVecPosition="+str(startingVecPosition)+", newMcStepNum="+str(newMcStepNum)+", newDataPointNum="+str(newDataPointNum))
        exit(0)

    #the rest of the cases is "equilibrium"

    #matching "equilibrium"
    matchEq=re.search(r"equilibrium",oneLine)
    if matchEq:
        continue

    #match lag
    matchLag=re.match(r"lag=(\d+)",oneLine)
    if matchLag:
        lag=int(matchLag.group(1))

    #match newDataPointNum
    matchNew=re.match(r"newDataPointNum=(\d+)",oneLine)
    if matchNew:
        newDataPointNum=int(matchNew.group(1))

    #match startingFileInd
    matchStartingFileInd=re.match(r"startingFileInd=(\d+)",oneLine)
    if matchStartingFileInd:
        startingFileInd=int(matchStartingFileInd.group(1))

    #match startingVecPosition
    matchStartingVecPosition=re.match(r"startingVecPosition=(\d+)",oneLine)
    if matchStartingVecPosition:
        startingVecPosition=int(matchStartingVecPosition.group(1))

newMcStepNum=lag*newDataPointNum

outDict={
    "startingFileInd":startingFileInd,
    "startingVecPosition":startingVecPosition,
    "newMcStepNum":newMcStepNum,
    "newDataPointNum":newDataPointNum

}
print(json.dumps(outDict))

exit(0)