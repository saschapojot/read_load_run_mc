import os
import subprocess
import sys
import re
import numpy as np
from pathlib import Path
from decimal import Decimal
import json

runName="run0"

confFileName="./confFiles/"+runName+".mc.conf"
invalidValueErrCode=1
summaryErrCode=2
loadErrCode=3
confErrCode=4
#parse conf
confResult=subprocess.run(["python3", "./init_run_scripts/parseConf.py", confFileName], capture_output=True, text=True)
if confResult.returncode !=0:
    print("Error running parseConf.py:")
    print(confResult.stderr)
    exit(confErrCode)

jsonDataFromConf = json.loads(confResult.stdout)
# print(confResult.stdout)
#read summary file
parseSummaryResult=subprocess.run(["python3","./init_run_scripts/search_and_read_summary.py", json.dumps(jsonDataFromConf)],capture_output=True, text=True)
if parseSummaryResult.returncode!=0:
    print("Error in parsing summary with code "+str(parseSummaryResult.returncode))
    exit(summaryErrCode)

jsonFromSummary=json.loads(parseSummaryResult.stdout)

# print(parseSummaryResult.stdout)


#load previous data, to get L, y0,z0,y1
loadResult=subprocess.run(["python3","./init_run_scripts/load_previous_data.py", json.dumps(jsonDataFromConf), json.dumps(jsonFromSummary)],capture_output=True, text=True)

if loadResult.returncode!=0:
    print("Error in parsing summary with code "+str(loadResult.returncode))
    exit(loadErrCode)
# print(loadResult.stdout)



#construct parameters that are passed to mc

TStr=jsonDataFromConf["T"]
funcName=jsonDataFromConf["potential_function_name"]
rowName=jsonDataFromConf["parameter_file_row"]
loopToWrite=jsonDataFromConf["loop_to_write"]

loadedJsonData=json.loads(loadResult.stdout)
LStr=loadedJsonData["L"]
y0Str=loadedJsonData["y0"]
z0Str=loadedJsonData["z0"]
y1Str=loadedJsonData["y1"]
loopLastFile=loadedJsonData["loopLastFile"]

jsonToCpp={
    "L":LStr,
    "y0":y0Str,
    "z0":z0Str,
    "y1":y1Str
}

newFlushNum=jsonFromSummary["newFlushNum"]

dataDir=jsonFromSummary["dataDir"]
U_Dir=jsonFromSummary["U_Dir"]
dist_Dir=jsonFromSummary["dist_Dir"]

parametersToCpp=[TStr,funcName,rowName,\
                 json.dumps(jsonToCpp),loopToWrite,newFlushNum\
                 ,loopLastFile,dataDir,U_Dir,dist_Dir]
parametersToCppStr=[str(elem) for elem in parametersToCpp]
# print("num of parameters to c++="+str(len(parametersToCpp)))


# cppExecutable="./run_mc"
#
# cppResult=subprocess.run([cppExecutable]+parametersToCppStr,capture_output=True, text=True)
# if cppResult.returncode!=0:
#     print("Error in cpp with code "+str(cppResult.returncode))
#
#
# print(cppResult.stdout)



#check summary for dist

checkDistErrCode=5
check_distResult=subprocess.run(["python3","./oneTCheckObservables/check_distOneT.py",json.dumps(jsonFromSummary)],capture_output=True, text=True)
if check_distResult.returncode!=0:
    print("Error in checking dist with code "+str(check_distResult.returncode))
    exit(checkDistErrCode)

print(check_distResult.stdout)