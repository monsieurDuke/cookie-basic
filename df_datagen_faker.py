import re
import time
import datetime

from faker import Faker
from termcolor import colored
from bug_logger import BugLogger

class DataFaker:

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

    def data_gen_proc(self, param):
        bug_logger = BugLogger()
        arg_sym = '>'
        try:
            arr_param = re.split('; |, |\ > ', param)
            if re.search('full-name', arr_param[1]):
                self.fake_name()
            elif re.search('email-address', arr_param[1]):
                self.fake_email()
            elif re.search('domain-name', arr_param[1]):
                self.fake_domain()
            elif re.search('full-date', arr_param[1]):
                self.fake_date()
            elif re.search('phone-number', arr_param[1]):
                self.fake_phone()
            elif re.search('street-address', arr_param[1]):
                self.fake_street()
            elif re.search('job-position', arr_param[1]):
                self.fake_job()
            else:
                print('Invalid argument: %s\n' % arr_param[1])
                print('| full-name    | email-address  | domain-name  | full-date |')
                print('| phone-number | street-address | job-position | ...       |\n')
                print("Please input the available argument in the correct format by adding the '%s' flag" % self.clr(arg_sym,'g'))
        except:
                curdate = datetime.datetime.now()
                fldate  = curdate.strftime('%m-%Y')
                print('Invalid argument: %s\n' % param)
                print('| full-name    | email-address  | domain-name  | full-date |')
                print('| phone-number | street-address | job-position | ...       |\n')
                print("Please input the available argument in the correct format by adding the '%s' flag" % self.clr(arg_sym,'g'))
                print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
                bug_logger.bug_logger_proc('DF')

    def timestop(self, go_time):
        frmt_query = '{:.3f}'.format(time.time() - go_time)
        str_result = '\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query)
        return str_result

    def heading(self, title):
        print(self.clr('Initializing Faker ...','c'))
        print(self.clr('Generating: '+title+' ...\n','c'))

    def fake_name(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('full-name (30)')
        for i in range(10):
            name_gen = '{:<21}'.format(fake_gen.name())
            print('|- %s' % (name_gen), end =' ')
            for i in range(1):
                name_gen = '{:<21}'.format(fake_gen.name())
                print('|- %s' % (name_gen), end =' ')
                for i in range(1):
                    name_gen = '{:<23}'.format(fake_gen.name())
                    print('|- %s' % (name_gen))
        print(self.timestop(go_time))

    def fake_email(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('email-address (20)')
        for i in range(10):
            email_gen = '{:<34}'.format(fake_gen.email())
            print('|- %s' % (email_gen), end =' ')
            for i in range(1):
                email_gen = '{:<26}'.format(fake_gen.email())
                print('|- %s' % (email_gen))
        print(self.timestop(go_time))

    def fake_domain(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('domain-address (30)')
        for i in range(10):
            domain_gen = '{:<21}'.format(fake_gen.domain_name())
            print('|- %s' % (domain_gen), end =' ')
            for i in range(1):
                domain_gen = '{:<21}'.format(fake_gen.domain_name())
                print('|- %s' % (domain_gen), end =' ')
                for i in range(1):
                    domain_gen = '{:<21}'.format(fake_gen.domain_name())
                    print('|- %s' % (domain_gen))
        print(self.timestop(go_time))

    def fake_date(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('full-date (30)')
        for i in range(10):
            domain_gen = '{:<21}'.format(fake_gen.domain_name())
            print('|- %s' % (domain_gen), end =' ')
            for i in range(1):
                domain_gen = '{:<21}'.format(fake_gen.domain_name())
                print('|- %s' % (domain_gen), end =' ')
                for i in range(1):
                    domain_gen = '{:<21}'.format(fake_gen.domain_name())
                    print('|- %s' % (domain_gen))
        print(self.timestop(go_time))

    def fake_phone(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('phone-number (30)')
        for i in range(10):
            phone_gen = '{:<15}'.format(str(fake_gen.phone_number())[:14])
            print('|- %s' % (phone_gen), end =' ')
            for i in range(1):
                phone_gen = '{:<15}'.format(str(fake_gen.phone_number())[:14])
                print('|- %s' % (phone_gen), end =' ')
                for i in range(1):
                    phone_gen = '{:<15}'.format(fake_gen.phone_number())[:14]
                    print('|- %s' % (phone_gen))
        print(self.timestop(go_time))

    def fake_street(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('street-address (10)')
        for i in range(10):
            add_gen = '{:<20}'.format(fake_gen.address())
            arr_add = re.split('; |, |\n', add_gen)
            print('|- '+arr_add[0]+', '+arr_add[1])
        print(self.timestop(go_time))

    def fake_job(self):
        fake_gen = Faker()
        go_time  = time.time()
        self.heading('job-position (10)')
        for i in range(10):
            job_gen = '{:<30}'.format(fake_gen.job())
            print('|- %s' % (job_gen))
        print(self.timestop(go_time))
