from oldLicenses.hardwareSerial import data
from oldLicenses.hardwareSerial import hardwareSerialNumber
from fileVariables import old_hw_log_path, computer_name, user_name
from lib.listToDictionary import dictionaryToList
from lib.uniqueList import make_unique
from lib.listToString import listToString


def convertDictTolist(data):
    hw_info = list()
    hardwares = data['Hardware'].split(',')
    print(hardwares)
    hardwares[0]=hardwares[0].split(" ")[0]
    serials = data['serials'].split(',')
    licenses = data['Licenses'].split(',')
    print(licenses)
    for i in range(0, len(serials)):
        serialNo = serials[i]
        hardware = hardwares[i]
        license = licenses[i]
        hw_info.append((serialNo, user_name, computer_name, hardware, license))
    return hw_info


def excelData(data):
    data_old = dict()
    hw_info = list()
    hardwares = data['Hardware'].split(',')
    hardwares[0] = hardwares[0].split(" ")[0]
    serials = data['serials'].split(',')
    licenses = data['Licenses'].split(',')
    for i in range(0, len(serials)):
        data_old['HW_Sr_No'] = serials[i]
        data_old['User_Name'] = user_name
        data_old['Comp_Name'] = computer_name
        data_old['HW_Name'] = hardwares[i]
        data_old['Licenses'] = licenses[i]
        data_old['Licenses_valid_upto']="-"
        data_old['debugger_Cable_serial_number']="-"
        hw_info.append(data_old.copy())
        data_old.clear()
    return hw_info


def get_data_from_vector_old_hw_log_file():
    hardwareSerialNumber()
    license = list()
    mainLicense_list = list()
    with open(old_hw_log_path, 'r') as file:
        for line in file:
            if "Licenses:" in line:
                for lines in file:
                    if lines == '\n':
                        mainLicense_list.append(license.copy())
                        license.clear()
                        break
                    else:
                        if '.' in line:
                            mainLicense_list.append(license.copy())
                            license.clear()
                            break
                        license.append(lines.strip() + "\n")
            else:
                continue

    # print(mainLicense_list)

    # print(data)
    License = dict()
    line_count = -1
    for license_data in mainLicense_list:
        if license_data:
            line_count += 1
            License[line_count] = license_data
    LicenseList = dictionaryToList(License)

    make_unique(LicenseList)
    LicenseList = listToString(LicenseList)
    data['Licenses'] = LicenseList

    hw_info = convertDictTolist(data)
    excel_data = excelData(data)

    return hw_info, excel_data
