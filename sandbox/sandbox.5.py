import os
import re
import sys
import datetime
import time

def bug_logger_proc():
    curdate = datetime.datetime.now()
    getdate = curdate.strftime('%d/%m/%Y')
    gettime = curdate.strftime('%I:%M:%S %p')
    error_info = str(sys.exc_info()[1])

    logs = open('buglogger.log', 'a')
    logs.write('[%s %s] (NS) ERROR: %s\n' % (getdate, gettime,error_info))
    logs.close()
    
try:
    num1  = int(input('Enter your initial : '))
    total = pow(num1/20, 2)
    print('current result is %s' % total)
except:
    bug_logger_proc()

