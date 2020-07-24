import smtplib
import sys
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

for email in range(5000):
	session.sendmail(sender_address, receiver_address, text)
	print('Mail Sent [%s]' % (email+1))
	time.sleep(0.5)
time.sleep(60)
session.quit()

