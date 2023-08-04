import os
hw_file_info_path = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client/vector_hw_info.csv"
hw_file_info_path_copy = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client/vector_hw_infocopy.csv"
Log_Path = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client/LogFile.log"
temp_file = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client//vector_hw_serial_info.txt"
old_hw_log_path = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client/report.log"
debugger_logfile_path="C:/Users/"+ os.getlogin() +"/AppData/Roaming/TRACE32/Debugger_License_Info.txt"
temp="C:/Users/" + os.getlogin() + "/AppData/Roaming/Vector/Vector License Client/tempdata.log"
db_server_name = "PU2S0017\SQLEXPRESS2017"
db_user_name = "hwtracker_db"
db_name = 'Hardware_Tracking'
db_password = "Test@123"

computer_name = os.environ['COMPUTERNAME']
user_name = os.getlogin()