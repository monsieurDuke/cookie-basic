import time
import sys
from clear_screen import clear

clear()
total_mail   = int(input('amount of emails : '))
sub_loop     = int(total_mail/55)
interval     = total_mail/55
counter      = 1
print(sub_loop)
print(interval)

print('________________________________________________________________________\n')
print('[+] Processing | ', end="", flush=True)
for i in range(55):
	if sub_loop < 1:
		for j in range(1):
			if counter <= total_mail:
				print('mail sent : %s' % (counter))
				counter += 1
				time.sleep(0.3)
	else:
		for j in range(sub_loop*2):
			if counter <= total_mail:
				print('mail sent : %s' % (counter))
				counter += 1
				time.sleep(0.3)
	prog = ':'
	print(prog, end="", flush=True)
	time.sleep(0.1)

print('\n[+] Finalizing | ', end="", flush=True)
for i in range(55):
	prog = ':'
	print(prog, end="", flush=True)
	time.sleep(0.1)
print()
