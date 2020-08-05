import os
columns, rows = os.get_terminal_size(0)

print('%s x %s' % (columns, rows))
