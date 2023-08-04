import linecache
import re

from fileVariables import Log_Path, computer_name, user_name, temp
from lib.listToString import listToString




def get_data_from_vector_new_hw_log_file():
    """ Function Name  : generate_log_vector_device_new_license
     Arguments      : none
     Return Value   : none
     Called By      : main
     Description    : generate log for vector Hw with old license"""
    data_new = dict()
    hw_info = list()
    database_data = list()
    count = 0
    log_file = open(Log_Path)
    log_lines = log_file.readlines()
    for lines in log_lines:
        count += 1
        license_info = []
        if re.search("SN.", lines):
            lin = lines.rpartition('Info;')[2]
            hw_name = lin.rpartition('(SN.')[0]
            lin1 = lines.rpartition('(SN. ')[2]
            hw_sr_no = lin1.rpartition(')')[0]
            lin2 = lines.rpartition('Info;')[2]
            lin2 = lines.rpartition('contains')[2]
            no_of_licenses = lin2.rpartition('licenses:')[0]
            if not no_of_licenses == "":
                for i in range(1, (int(no_of_licenses) + 1)):
                    next_line = linecache.getline(Log_Path, count + i)
                    if re.search(";>> ", linecache.getline(Log_Path, count + i)):
                        lin1 = next_line.rpartition('Info;>> ')[2]
                        licenses = lin1.rpartition('\n')[0]
                        license_info.append(licenses)
            print(no_of_licenses)
            count=0;
            if  no_of_licenses != "":
                for i in range(1, (int(no_of_licenses) + 1)):
                    count+=1
                    next_line = linecache.getline(Log_Path, count + i)
                    print(next_line)
                    print(linecache.getline(Log_Path, count + i))
                    if re.search(";>> ", linecache.getline(Log_Path, count + i)):
                        lin1 = next_line.rpartition('Info;>> ')[2]
                        licenses = lin1.rpartition('\n')[0]
                        license_info.append(licenses)
                license_info = listToString(license_info)
                hw_sr_no = hw_sr_no.split(" ")[0]
                data_new['HW_Sr_No'] = hw_sr_no
                data_new['User_Name'] = user_name
                data_new['Comp_Name'] = computer_name
                data_new['HW_Name'] = hw_name
                data_new['Licenses'] = license_info
                data_new['Licenses_valid_upto']=expireDate()[0]
                data_new['debugger_Cable_serial_number']="-"
                count+=1
                hw_info.append(data_new.copy())
                database_data.append((hw_sr_no, user_name, computer_name, hw_name, license_info,data_new['Licenses_valid_upto']))
                data_new.clear()
    log_file.close()
    print(database_data)
    return hw_info,database_data

def expireDate():
    f = open(temp, 'r+')
    data = list()
    for i in f.readlines():
        if "<ExpirationDateString>" in i:
            data.append(i.split('>')[1].split('<')[0])
    unique = dict()
    for i in data:
        unique[i] = ""
    data = list(unique.keys())
    return data