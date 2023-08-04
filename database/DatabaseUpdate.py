import sys
import pymssql
import argparse
import threading

class DataBaseOperations:

    def __init__(self, db_server, db_user, db_name, db_password):
        """
        '''Initialize'''
        :param db_server:
        :param db_user:
        :param password:
        :param database_name:
        """
        self.db_server = db_server
        self.db_name = db_name
        self.db_password = db_password
        self.username = db_user

    def update_TM_Project_table_debugger(self, serial_no, pc_name, user_name, hardware_name, licenses, Datevalue, Timevalue,
                                    Licenses_valid_upto="-",
                                    debugger_Cable_serial_number="-"):
            """
            Add the projects into Project table for the specified Base Project if not present
            :param project:
            :param base_project:
            :return: Project ID
            """
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT MAX([RowID]) FROM [Hardware_Tracking].[dbo].[HardwareInfo] WHERE'
                               '[SerialNumber] = %s', (serial_no))
                rowid = cursor.fetchone()[0]
                if rowid is None:
                    # print("\n::Adding Project-->", project,"::")
                    cursor.execute(
                        "INSERT INTO [Hardware_Tracking].[dbo].[HardwareInfo] ([SerialNumber],[PCName],[UserName],\
                        [HardwareName],[Licenses],[Date],[time],[Licenses_valid_upto],[debugger_Cable_serial_number]) "
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                        serial_no, pc_name, user_name, hardware_name, licenses, Datevalue, Timevalue,
                        Licenses_valid_upto, debugger_Cable_serial_number))
                    self.conn.commit()
                    return rowid
                else:
                    data = (
                    serial_no, user_name, pc_name, hardware_name, licenses, Datevalue, Timevalue, Licenses_valid_upto,
                     debugger_Cable_serial_number, rowid)

                    cursor.execute("update  HardwareInfo set SerialNumber=%s, UserName=%s,PCName=%s \
    ,HardwareName=%s,Licenses=%s,Date=%s,time=%s,Licenses_valid_upto=%s,\
    debugger_Cable_serial_number=%s where RowID=%d ", data)

                    self.conn.commit()

            except Exception as e:
                print("::::Problem Occurred while executing the SQL query::::")
                print(e)
                sys.exit(-1)

    def update_TM_Project_table(self, serial_no, pc_name, user_name, hardware_name, licenses,Datevalue ,Timevalue,Licenses_valid_upto=" ",debugger_Cable_serial_number=" " ):
        """
        Add the projects into Project table for the specified Base Project if not present
        :param project:
        :param base_project:
        :return: Project ID
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT MAX([RowID]) FROM [Hardware_Tracking].[dbo].[HardwareInfo] WHERE'
                           '[SerialNumber] = %s', (serial_no))
            rowid = cursor.fetchone()[0]
            if rowid is None:
                # print("\n::Adding Project-->", project,"::")
                cursor.execute(
                    "INSERT INTO [Hardware_Tracking].[dbo].[HardwareInfo] ([SerialNumber],[PCName],[UserName],\
                    [HardwareName],[Licenses],[Date],[time],[Licenses_valid_upto],[debugger_Cable_serial_number]) "
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (serial_no, pc_name, user_name, hardware_name, licenses,Datevalue,Timevalue,Licenses_valid_upto,debugger_Cable_serial_number))
                self.conn.commit()
                return rowid
            else:
                data= (serial_no,user_name,pc_name,hardware_name, licenses,Datevalue,Timevalue ,Licenses_valid_upto,debugger_Cable_serial_number,rowid)

                cursor.execute("update  HardwareInfo set SerialNumber=%s, UserName=%s,PCName=%s \
,HardwareName=%s,Licenses=%s,Date=%s,time=%s,Licenses_valid_upto=%s,\
debugger_Cable_serial_number=%s where RowID=%d ",data)

                self.conn.commit()

        except Exception as e :
            print("::::Problem Occurred while executing the SQL query::::")
            print(e)
            sys.exit(-1)
    def connect_to_sql(self):
        """
        Connect to SQL Database Server
        :return: 0 if connection successful!!
        """
        try:
            self.conn = pymssql.connect(self.db_server, self.username, self.db_name, self.db_password)
            return 0
        except Exception:
            print("::::Problem in establishing database server connection \n verify the credentials or"
                  " try to login manually::::")
            sys.exit(-1)

def process_cmdl_args():
    global serial_no, pc_name, user_name, hardware_name, licenses
    parser = argparse.ArgumentParser(description="Script Insert data to DB")
    parser.add_argument("-serial_no", "--serial_no", type=str, nargs=1,
                        default=None, required=True,
                        help="Give serial number of Device")
    parser.add_argument("-pc_name", "--pc_name", type=str, nargs=1,
                        default=None, required=True,
                        help="Provide PC Name")
    parser.add_argument("-user_name", "--user_name", type=str, nargs=1,
                        default=None, required=True,
                        help="Provide user name")
    parser.add_argument("-hardware_name", "--hardware_name", type=str, nargs=1,
                        default=None, required=True,
                        help="Provide hardware Name")
    parser.add_argument("-licenses", "--licenses", type=str, nargs=1,
                        default=None, required=True,
                        help="licenses")

    args = parser.parse_args()
    serial_no = args.serial_no[0]
    pc_name = args.pc_name[0]
    user_name = args.user_name[0]
    hardware_name = args.hardware_name[0]
    licenses = args.licenses[0]





if __name__ == '__main__':

    process_cmdl_args()
    db_server_name = "PU2S0017\SQLEXPRESS2017"
    db_user_name = "hwtracker_db"
    db_name = "Hardware_Tracking"
    db_password = "Test@123"

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::DataBaseOperations Class object creation and variable initialisation::::::::::::::::
    db_handler = DataBaseOperations(db_server_name, db_user_name, db_password, db_name)

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::Establish connection with database::::::::::::::::::::::::
    connect_status = db_handler.connect_to_sql()
    if connect_status == 0:  # database successfully connected
        print("::::Database connection successfully established::::")

    threading.Thread(db_handler.update_TM_Project_table,args=(serial_no, pc_name, user_name, hardware_name, licenses , DateValue , timeValue,Licenses_valid_upto,debugger_Cable_serial_number))