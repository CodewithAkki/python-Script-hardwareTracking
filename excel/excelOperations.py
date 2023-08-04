import os
import csv
from fileVariables import hw_file_info_path, old_hw_log_path, Log_Path,hw_file_info_path_copy
from lib.databaseOperations import database_update


def update_hw_vector_info(data_new, database_data_old, database_data_new , result_debugger_data) :
    print(data_new)
    if not data_new:
        os.remove(hw_file_info_path)
        print("log:>> file" + hw_file_info_path + " is removed...")

    fields = ["HW_Sr_No", "User_Name", "Comp_Name", "HW_Name", "Licenses","Licenses_valid_upto","debugger_Cable_serial_number"]
    if not os.path.exists(hw_file_info_path):
        with open(hw_file_info_path, 'w+', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data_new)
            f.close()
            for hw_info in database_data_new:
                if '' != hw_info:
                    database_update(hw_info)
                    if os.path.exists(Log_Path):
                        os.remove(Log_Path)
                    if os.path.exists(old_hw_log_path):
                        os.remove(old_hw_log_path)


            for hw_info in database_data_old:
                if '' != hw_info:
                    database_update(hw_info)
                    if os.path.exists(Log_Path):
                        os.remove(Log_Path)
                    if os.path.exists(old_hw_log_path):
                        os.remove(old_hw_log_path)

            for hw_info in result_debugger_data:
                if '' != hw_info:
                    database_update(hw_info)
                    if os.path.exists(Log_Path):
                        os.remove(Log_Path)
                    if os.path.exists(old_hw_log_path):
                        os.remove(old_hw_log_path)
    else:
        with open(hw_file_info_path, 'w+', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data_new)
            f.close()
        for hw_info in database_data_new:
            print(hw_info)
            if hw_info != '':
                database_update(hw_info)
                if os.path.exists(Log_Path):
                    os.remove(Log_Path)
                if os.path.exists(old_hw_log_path):
                    os.remove(old_hw_log_path)

        for hw_info in database_data_old:
            if hw_info[0] != '':
                database_update(hw_info)
                if os.path.exists(Log_Path):
                    os.remove(Log_Path)
                if os.path.exists(old_hw_log_path):
                    os.remove(old_hw_log_path)

        for hw_info in result_debugger_data:
            if '' != hw_info:
                database_update(hw_info)
                if os.path.exists(Log_Path):
                    os.remove(Log_Path)
                if os.path.exists(old_hw_log_path):
                    os.remove(old_hw_log_path)

        '''with open(hw_file_info_path_copy, 'r+', encoding='UTF8', newline='') as f:
            dict_reader = csv.DictReader(f)
            list_of_dictcopy = list(dict_reader)
            f.close()

        with open(hw_file_info_path, 'r+', encoding='UTF8', newline='') as f:
            dict_reader = csv.DictReader(f)
            list_of_dict = list(dict_reader)
            f.close()
            if list_of_dict == list_of_dictcopy:
                print('log:>> already in database')
                os.remove(Log_Path)
                os.remove(old_hw_log_path)
            else:
                for data in range(0, len(list_of_dictcopy)):
                    for data_csv in range(0, len(list_of_dict)):
                        if list_of_dictcopy[data] == list_of_dict[data_csv]:
                            list_of_dictcopy[data] = dict()
                print(list_of_dictcopy)
                data_csv = list()
                for data in list_of_dictcopy:
                    if data == {}:
                        continue
                    else:
                        data_csv.append(data)
                print(":::remaining records:::"+data_csv)
                with open(hw_file_info_path, 'w+', encoding='UTF8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.append()
                    f.close()
                print("remaining::", data_csv)

                if len(data_csv) > 0:
                    for data in data_csv:
                        for data__new in database_data_new:
                            if data['HW_Sr_No'] in data__new:
                                database_update(data__new)
                                os.remove(Log_Path)
                                os.remove(old_hw_log_path)

                    for data in data_csv:
                        for data__new in database_data_old:
                            if data['HW_Sr_No'] in data__new:
                                database_update(data__new)
                                os.remove(Log_Path)
                                os.remove(old_hw_log_path)'''
