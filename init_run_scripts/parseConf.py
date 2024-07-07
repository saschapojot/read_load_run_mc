import re
import sys
# inConfFile="./confFiles/run0.mc.conf"
import json

#this script parse conf file and return the parameters as json data
fmtErrStr="format error: "
fmtCode=1
valueMissingCode=2
paramErrCode=3
if (len(sys.argv)!=2):
    print("wrong number of arguments.")
    exit(paramErrCode)
inConfFile=sys.argv[1]


def removeCommentsAndEmptyLines(file):
    """

    :param file: conf file
    :return: contents in file, with empty lines and comments removed
    """
    with open(file,"r") as fptr:
        lines= fptr.readlines()

    linesToReturn=[]
    for oneLine in lines:
        oneLine = re.sub(r'#.*$', '', oneLine).strip()
        if not oneLine:
            continue
        else:
            linesToReturn.append(oneLine)
    return linesToReturn


def parseConfContents(file):
    """

    :param file: conf file
    :return:
    """
    lineWithCommentsRemoved=removeCommentsAndEmptyLines(file)
    TList=""
    eraseData=""
    searchReadSmrFile=""
    SearchLoadData=""
    obs_name=""
    potFuncName=""
    paramFile=""
    rowNum=""


    float_pattern = r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?'
    TList_pattern = rf'\[({float_pattern}(?:,{float_pattern})*)\]'
    boolean_pattern = r'(true|false)'

    for oneLine in lineWithCommentsRemoved:
        matchLine=re.match(r'(\w+)\s*=\s*(.+)', oneLine)
        if matchLine:
            key = matchLine.group(1).strip()
            value = matchLine.group(2).strip()
            # print("value="+value)
            #match T
            if key=="T":
                matchList=re.match(TList_pattern,value)
                if matchList:
                    TList=matchList.group(1)
                else:
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)


            #match erase_data_if_exist
            if key=="erase_data_if_exist":
                matchErase=re.match(boolean_pattern,value,re.IGNORECASE)
                if matchErase:
                    eraseData=matchErase.group(1)
                    eraseData=eraseData.capitalize()
                else:
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)

            #match search_and_read_summary_file
            if key=="search_and_read_summary_file":
                matchSmr=re.match(boolean_pattern,value,re.IGNORECASE)
                if matchSmr:
                    searchReadSmrFile=matchSmr.group(1)
                    searchReadSmrFile=searchReadSmrFile.capitalize()
                else:
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)

            #match search_and_load_previous_data
            if key=="search_and_load_previous_data":
                matchLoad=re.match(boolean_pattern,value,re.IGNORECASE)
                if matchLoad:
                    SearchLoadData=matchLoad.group(1)
                    SearchLoadData=SearchLoadData.capitalize()

                else:
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)

            #match observable_name
            if key=="observable_name":
                #if matching a non word character
                if re.search(r"[^\w]",value):
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)

                obs_name=value

            if key=="potential_function_name":
                #if matching a non word character
                if re.search(r"[^\w]",value):
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)
                potFuncName=value

            if key=="parameter_file":
                paramFile=value

            if key=="parameter_file_row":
                #if matching a non digit character
                if re.search(r"[^\d]",value):
                    print(fmtErrStr+oneLine)
                    exit(fmtCode)
                rowNum=value

        else:
            print("line: "+oneLine+" is discarded.")
            continue

    if TList=="":
        print("T not found in "+str(file))
        exit(valueMissingCode)
    if eraseData=="":
        print("erase_data_if_exist not found in "+str(file))
        exit(valueMissingCode)
    if searchReadSmrFile=="":
        print("search_and_read_summary_file not found in "+str(file))
        exit(valueMissingCode)

    if SearchLoadData=="":
        print("search_and_load_previous_data not found in "+str(file))
        exit(valueMissingCode)

    #do not check if observable exists

    if potFuncName=="":
        print("potential_function_name not found in "+str(file))
        exit(valueMissingCode)
    if paramFile=="":
        print("parameter_file not found in "+str(file))
        exit(valueMissingCode)
    if rowNum=="":
        print("parameter_file_row not found in "+str(file))
        exit(valueMissingCode)

    if obs_name=="":
        dictTmp={
            "T":TList,
            "erase_data_if_exist":eraseData,
            "search_and_read_summary_file":searchReadSmrFile,
            "search_and_load_previous_data":SearchLoadData,
            "potential_function_name":potFuncName,
            "parameter_file":paramFile,
            "parameter_file_row":rowNum
        }
        return dictTmp
    else:
        dictTmp={
            "T":TList,
            "erase_data_if_exist":eraseData,
            "search_and_read_summary_file":searchReadSmrFile,
            "search_and_load_previous_data":SearchLoadData,
            "observable_name":obs_name,
            "potential_function_name":potFuncName,
            "parameter_file":paramFile,
            "parameter_file_row":rowNum
        }
        return dictTmp




dataJson=parseConfContents(inConfFile)
print(json.dumps(dataJson))