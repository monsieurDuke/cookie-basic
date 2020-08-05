import datetime
import os
import sys

class BugLogger:

    def bug_logger_proc(self, menu):
        curdate = datetime.datetime.now()
        getdate = curdate.strftime('%d/%m/%Y')
        gettime = curdate.strftime('%I:%M:%S %p')
        error_info = str(sys.exc_info()[1])
        if error_info == '':
            error_info = 'action have been manually cancled by user (ctrl + c)'
        error_frm = '[%s %s] (%s) ERROR: %s\n' % (getdate, gettime, menu, error_info)
        logs = open(str(os.getcwd())+'/log/bug-tracker.log', 'a')
        logs.write(error_frm)
        logs.close()
