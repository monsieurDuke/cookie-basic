import os
import sys

rows, columns = os.popen('stty size', 'r').read().split()
linez = ['_']*(int(columns)-2)
line  = ''.join(map(str, linez))
print("Your terminal's width is: %s" % columns)
print(line)
