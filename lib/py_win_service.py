# uncomment mainthread() or mainloop() call below
# run without parameters to see HandleCommandLine options
# install service with "install" and remove with "remove"
# run with "debug" to see print statements
# with "start" and "stop" watch for files to appear
# check Windows EventViever for log messages

import socket
import sys
import threading
import time
from random import randint
from os import path

import servicemanager
import win32event
import win32service
import win32serviceutil
# see http://timgolden.me.uk/pywin32-docs/contents.html for details


def dummytask_once(msg='once'):
    fn = path.join(path.dirname(__file__),
                '%s_%s.txt' % (msg, randint(1, 10000)))
    with open(fn, 'w') as fh:
        print(fn)
        fh.write('')


def dummytask_loop():
    global do_run
    while do_run:
        dummytask_once(msg='loop')
        time.sleep(3)


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global do_run
        do_run = True
        print('thread start\n')
        dummytask_loop()
        print('thread done\n')

    def exit(self):
        global do_run
        do_run = False


class SMWinservice(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PyWinSvc'
    _svc_display_name_ = 'Python Windows Service'
    _svc_description_ = 'An example of a windows service in Python'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stopEvt = win32event.CreateEvent(None, 0, 0, None)  # create generic event
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STOPPED,
                            (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stopEvt)  # raise event

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        # UNCOMMENT ONE OF THESE
        # self.mainthread()
        # self.mainloop()

    # Wait for stopEvt indefinitely after starting thread.
    def mainthread(self):
        print('main start')
        self.server = MyThread()
        self.server.start()
        print('wait for win32event')
        win32event.WaitForSingleObject(self.stopEvt, win32event.INFINITE)
        self.server.exit()
        print('wait for thread')
        self.server.join()
        print('main done')

    # Wait for stopEvt event in loop.
    def mainloop(self):
        print('loop start')
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            dummytask_once()
            rc = win32event.WaitForSingleObject(self.stopEvt, 3000)
        print('loop done')


if __name__ == '__main__':
    SMWinservice.parse_command_line()
