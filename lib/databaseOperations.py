from database.DatabaseUpdate import DataBaseOperations
from fileVariables import db_password, db_name, db_user_name, db_server_name
import datetime

def database_update(hw_data):
    # db_handler = connect_database()
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::DataBaseOperations Class object creation and variable initialisation::::::::::::::::
    db_handler = DataBaseOperations(db_server_name, db_user_name, db_password,
                                    db_name)  # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::Establish connection with database::::::::::::::::::::::::
    connect_status = db_handler.connect_to_sql()
    if connect_status == 0:  # database successfully connected

        # return db_handler

        hardware_name = hw_data[3]
        if hardware_name!='' and hardware_name!='debugger':
            print(hw_data)
            print("::::Database connection successfully established::::")
            hw_data = list(hw_data)
            serial_no = hw_data[0]
            user_name = hw_data[1]
            pc_name = hw_data[2]
            licenses = str(hw_data[4])
            date = datetime.datetime.now()
            t_hour = date.time().hour
            t_min = date.time().minute
            t_time = str(t_hour) + ":" + str(t_min)
            if hardware_name != 'debugger':
                if len(hw_data)==6:
                    l_v_upto = hw_data[5].split("T")
                    Licenses_valid_upto=l_v_upto[0]+"   T"+l_v_upto[1]
                    debugger_Cable_serial_number = "-"
                else:
                    Licenses_valid_upto=debugger_Cable_serial_number="-"
                db_handler.update_TM_Project_table(serial_no, pc_name, user_name, hardware_name, licenses,str(date.date()),t_time,Licenses_valid_upto,debugger_Cable_serial_number)
            else:
                Licenses_valid_upto=hw_data[5]
                debugger_Cable_serial_number=hw_data[6]
                db_handler.update_TM_Project_table(serial_no, pc_name, user_name, hardware_name, licenses, str(date.date()),t_time,Licenses_valid_upto,debugger_Cable_serial_number)
        if hardware_name == 'debugger':
            hw_data = list(hw_data)
            print(hw_data ,"",hardware_name)
            user_name = hw_data[-1]
            pc_name = hw_data[-3]
            licenses = str(hw_data[2])
            date = datetime.datetime.now()
            t_hour = date.time().hour
            t_min = date.time().minute
            t_time = str(t_hour) + ":" + str(t_min)
            Licenses_valid_upto = hw_data[-2]
            serial_no =hw_data[0].replace('/','')
            debugger_Cable_serial_number=hw_data[1]
            db_handler.update_TM_Project_table_debugger(serial_no, pc_name, user_name, hardware_name, licenses, str(date.date()),
                                               t_time, Licenses_valid_upto,
                                               debugger_Cable_serial_number)

