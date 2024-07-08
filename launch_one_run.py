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
#parse conf
confResult=subprocess.run(["python3", "./init_run_scripts/parseConf.py", confFileName], capture_output=True, text=True)
if confResult.returncode !=0:
    print("Error running parseConf.py:")
    print(confResult.stderr)

jsonDataFromConf = json.loads(confResult.stdout)
print(confResult.stdout)
#read summary file
parseSummaryResult=subprocess.run(["python3","./init_run_scripts/search_and_read_summary.py", json.dumps(jsonDataFromConf)],capture_output=True, text=True)
if parseSummaryResult.returncode!=0:
    print("Error in parsing summary with code "+str(parseSummaryResult.returncode))
    exit(summaryErrCode)

jsonFromSummary=json.loads(parseSummaryResult.stdout)

print(parseSummaryResult.stdout)


#load previous data, to get L, y0,z0,y1
loadResult=subprocess.run(["python3","./init_run_scripts/load_previous_data.py", json.dumps(jsonDataFromConf), json.dumps(jsonFromSummary)],capture_output=True, text=True)

if loadResult.returncode!=0:
    print("Error in parsing summary with code "+str(loadResult.returncode))
    exit(loadErrCode)
# print(loadResult.stdout)



#construct parameters that are passed to mc

TStr=jsonDataFromConf["T"]
funcName=jsonDataFromConf["potential_function_name"]