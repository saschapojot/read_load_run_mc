import sys
numArgErr=4
import json
from decimal import Decimal

#this script loads previous data

if (len(sys.argv)!=3):
    print("wrong number of arguments.")
    exit(numArgErr)

jsonDataFromConf =json.loads(sys.argv[1])
jsonFromSummary=json.loads(sys.argv[2])

potential_function_name=jsonDataFromConf["potential_function_name"]
parameter_file_row=int(jsonDataFromConf["parameter_file_row"])
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



dataDir="./dataAll/"+potential_function_name+"/row"+str(parameter_file_row)+"/T"+str(TVal)+"/"

pickleDir=dataDir+"/dist_AllPickle/"