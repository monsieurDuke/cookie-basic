import smtplib
import sys
#from tqdm import tqdm
#from tqdm import trange
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_content = "Halo Mamah,\nSelamat Malam\n\naku menyampaikan pesan ini karena aku mau bowbow. Dadah\n\nBlack Ice"

sender_address   = 'icatmuhammad3@gmail.com'
sender_pass      = 'wuooppacgpugsups'
receiver_address = 'icatmuhammad2@gmail.com'

#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'Pesan dari Snowy, The Black Ice'

#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))

#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(sender_address, sender_pass)
text = message.as_string()

#Progress bar
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
				session.sendmail(sender_address, receiver_address, text)
				print('mail sent : %s' % (counter))
				counter += 1
				time.sleep(0.3)
	else:
		for j in range(sub_loop*2):
			if counter <= total_mail:
				session.sendmail(sender_address, receiver_address, text)
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

#for email in range(5000):
#	print('Mail Sent [%s]' % (email+1))
#	time.sleep(0.5)
#time.sleep(60)

session.quit()

