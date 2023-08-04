from fileVariables import debugger_logfile_path, computer_name, user_name


def debugger_licence():
    licence_data = list()
    data_list = list()
    debugger_cable_serial_number = ""
    data_debugger_dictionary = dict()
    data_debugger_dictionary_list = list()
    log_file = open(debugger_logfile_path, 'r')
    log_lines = log_file.readlines()
    setvalue=0
    for nextline in log_lines:

        if 'Debug Cable' in nextline:
            debug_line = nextline.split(' ')
            try:
                if debug_line[2]:
                    debugger_cable_serial_number = debug_line[2].strip().split(':')[0]
            except IndexError:
                debugger_cable_serial_number = ""
            licence = log_lines[log_lines.index(nextline) + 1].strip()
            debugger_serial_no = log_lines[log_lines.index(nextline) + 1].strip().split(':')[0]
            licence_data.append(debugger_cable_serial_number.strip())
            licence_data.append(debugger_serial_no.strip())

        if 'Features' in nextline:
            feature = nextline.split(':')[1].strip()
            licence += " " + feature
            licence=licence.split(":")[1];
            licence_data.append(licence)
            licence=""

        if 'Maintenance' in nextline:
            licence_valid_upto = nextline.split(':')[1].split(" ")[5]
            licence_data.append("debugger")
            licence_data.append(computer_name)
            licence_data.append(licence_valid_upto)
            licence_data.append(user_name)
            if licence_data[0]:
                licence_data[0]+='/'+licence_data[1]
            else:
                licence_data[0]=licence_data[1]
                licence_data[1]="-"
            list_data = licence_data.copy()
            licence_data.clear()
            data_list.append(list_data)

        else:
            if 'family' in nextline and licence=="":
                licence = nextline
                debugger_serial_no = licence.split(':')[0]
                debugger_serial_no = debugger_serial_no.strip()
                if debugger_serial_no in licence_data:
                    continue
                else:
                    licence_data.append(" ")
                    licence_data.append(debugger_serial_no)





    print(data_list)
    for i in data_list:

        data_debugger_dictionary['debugger_Cable_serial_number'] = i[1]
        data_debugger_dictionary['HW_Sr_No'] = i[0].replace('/','')
        data_debugger_dictionary['Licenses'] = i[2]
        data_debugger_dictionary['User_Name'] = user_name
        data_debugger_dictionary['Comp_Name'] = computer_name
        data_debugger_dictionary['Licenses_valid_upto'] = i[-2]
        data_debugger_dictionary['HW_Name'] = "debugger"
        print(data_debugger_dictionary)
        data_debugger_dictionary_list.append(data_debugger_dictionary)

    return data_list, data_debugger_dictionary_list
