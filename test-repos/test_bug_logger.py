import datetime
import os
import sys
import pytest

class TestBugLogger:

    def test_bug_logger_proc(self):
        curdate = datetime.datetime.now()
        getdate = curdate.strftime('%d/%m/%Y')
        fldate  = curdate.strftime('%m-%Y')
        gettime = curdate.strftime('%I:%M:%S %p')
        error_info = str(sys.exc_info()[1])
        if error_info == '':
            error_info = 'action have been manually cancled by user (ctrl + c)'
        error_frm = '[%s %s] (..) ERROR: %s\n' % (getdate, gettime, error_info)
        logs = (str(os.getcwd())+'/'+fldate+'.bug.log', "a+")
        print('%s :: %s ' % (logs, error_frm))
