import datetime
import os
import subprocess
import sys
import threading

import win32com.client
import win32com.client
from win32com.client import GetObject

from debugger import getDebuggerLicenses
from excel.excelOperations import update_hw_vector_info
from fileVariables import old_hw_log_path, Log_Path, temp, debugger_logfile_path
from newLicenses.mainFile import get_data_from_vector_new_hw_log_file
from oldLicenses.mainFile import get_data_from_vector_old_hw_log_file

global device_no

def task_schedular():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    # Defining the Start time of job
    start_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

    # For Daily Trigger set this variable to 2 ; for One time run set this value as 1
    TASK_TRIGGER_DAILY = 2
    trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)

    # Repeat for a duration of number of day
    num_of_days = 10
    trigger.Repetition.Duration = "P" + str(num_of_days) + "D"

    # use PT2M for every 2 minutes, use PT1H for every 1 hour
    trigger.Repetition.Interval = "PT1M"
    trigger.StartBoundary = start_time.isoformat()

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'TRIGGER BATCH'
    #action.Path = 'C:\\KBData\\test.bat'
    action.Path = "C:\\Users\\ext-mitharia\\PycharmProjects\\HardwareFinder\\main.pyw"
    #action.Arguments = '/c start /min "" "C:\\KBData\\test.bat"'

    # Set parameters
    task_def.RegistrationInfo.Description = 'Test Task'
    task_def.Settings.Enabled = True

    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.Hidden = True

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        'Test Task',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE
    )


def generate_log_vector_device_old_license():
    """
     Function Name  : generate_log_vector_device_old_license
     Arguments      : none
     Return Value   : none
     Called By      : main
     Description    : generate log for vector Hw with old license"""

    command = "vcanconf.exe -genConfReport:" + old_hw_log_path
    if os.path.exists(old_hw_log_path):
        try:
            os.system(command)
        except os.error as exc:
            print("Status : FAIL", exc.returncode, exc.output)
            print("Log generation failed for Vector devices having old license...")
            exit(-1)
    else:
        open(old_hw_log_path, "w+")
        print('log :>> report file created')
        if os.path.exists(old_hw_log_path):
            try:
                os.system(command)
            except os.error as exc:
                print("Status : FAIL", exc.returncode, exc.output)
                print("Log generation failed for Vector devices having old license...")
                exit(-1)


def generate_log_vector_device_new_license():
    """
      Function Name  : generate_log_vector_device_new_license
      Arguments      : none
      Return Value   : none
      Called By      : main
      Description    : generate log for vector Hw with old license"""



    try:
        command = "C:/Program Files (x86)/Vector License Client/Vector.LicenseClient"
        # if log file available before batch command, remove log file.
        f=open(temp,"w+")
        if os.path.exists(Log_Path):
            os.remove(Log_Path)
        sys.stdout.flush()
        subprocess.call([command, "-listLicenses"], stdin=subprocess.PIPE,stdout=f)
        f.close()
        os.system('cls')



        if os.path.isfile(Log_Path):
            print('log :>>log file generated at ', Log_Path)
        else:
            print('log :>>Failure....log file not generated at ', Log_Path)
            exit(-1)

    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        print("Log generation failed for Vector devices having new license ...")
        exit(-1)

def generate_log_for_debugger_device():
    if os.path.exists(debugger_logfile_path) == False:
        open(debugger_logfile_path,'w+')




def main_function():
    task_schedular()
    generate_log_for_debugger_device()
    generate_log_vector_device_new_license()
    generate_log_vector_device_old_license()


    data_new, database_data_new = get_data_from_vector_new_hw_log_file()
    database_data_old, data_old = get_data_from_vector_old_hw_log_file()
    result_debugger_data , debugger_dictionary = getDebuggerLicenses.debugger_licence()
    print(debugger_dictionary)

    #[{'HW_Sr_No': '', 'User_Name': 'ext-mitharia', 'Comp_Name': 'PU2L6174', 'HW_Name': '', 'Licenses': ''}]
    for data in data_old:
        if data['HW_Name'] != '':
            data_new.append(data)
    for data in debugger_dictionary:
        if data['HW_Name'] != '':
            data_new.append(data)
    target = update_hw_vector_info(data_new, database_data_old, database_data_new, result_debugger_data)

def deletefile():
    if os.path.exists(debugger_logfile_path):
        os.remove(debugger_logfile_path)

if __name__ == '__main__':
    threading.Thread(main_function()).start()
    threading.Thread(deletefile()).start()
    #close
    WMI = GetObject('winmgmts:')
    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
        os.system("taskkill /pid " + str(p.ProcessId))










