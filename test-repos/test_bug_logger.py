import datetime
import os
import sys
import pytest

class TestBugLogger:

    def test_bug_logger_proc(self):
        curdate = datetime.datetime.now()
        getdate = curdate.strftime('%d/%m/%Y')
        gettime = curdate.strftime('%I:%M:%S %p')
        error_info = str(sys.exc_info()[1])
        menu_alias = 'Pytest'
        if error_info == '':
            error_info = 'action have been manually cancled by user (ctrl + c)'
        error_frm = '[%s %s] (%s) ERROR: %s\n' % (getdate, gettime, menu_alias, error_info)
        #logs = open(str(os.getcwd())+'/log/bug-tracker.log', 'a')
        #logs.write(error_frm)
        #logs.close()
