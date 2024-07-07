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
#parse conf
confResult=subprocess.run(["python3", "./init_run_scripts/parseConf.py", confFileName], capture_output=True, text=True)
if confResult.returncode !=0:
    print("Error running parseConf.py:")
    print(confResult.stderr)

jsonData = json.loads(confResult.stdout)


T_list_str = jsonData['T']
T_list = [float(value) for value in T_list_str.split(',')]
#check if T values are positive numbers
for val in T_list:
    if val<=0:
        print("invalid temperature: "+str(val))
        exit(invalidValueErrCode)

erase_data_if_exist=bool(jsonData["erase_data_if_exist"])
search_and_read_summary_file=bool(jsonData["search_and_read_summary_file"])
search_and_load_previous_data=bool(jsonData["search_and_load_previous_data"])
potential_function_name=jsonData["potential_function_name"]
parameter_file=jsonData["parameter_file"]
parameter_file_row=int(jsonData["parameter_file_row"])



#run T_list[0]

def format_using_decimal(value):
    # Convert the float to a Decimal
    decimal_value = Decimal(value)
    # Remove trailing zeros and ensure fixed-point notation
    formatted_value = decimal_value.quantize(Decimal(1)) if decimal_value == decimal_value.to_integral() else decimal_value.normalize()
    return str(formatted_value)

TVal=format_using_decimal(T_list[0])

dataDir="./dataAll/"+potential_function_name+"/row"+str(parameter_file_row)+"/T"+str(TVal)+"/"

makeNewSummaryFile=False