import datetime, time, os, os.path
import sys, decimal, re, pytest

from termcolor import colored
from clear_screen import clear
from os import path

from bug_logger import BugLogger
from ro_ciphergen_rot13 import CipherROT13
from ns_network_scanner import NetworkScanner
from ps_port_scanner import PortScanner
from sf_subnet_finder import SubnetFinder
from df_datagen_faker import DataFaker
from mb_mail_bomber import MailBomber
from rs_ciphergen_rsa import CipherRSA

class CookieBasic:

	def header(self):
		clear()
		x_row, y_columns = os.popen('stty size', 'r').read().split()
		columns   = 109
		rows      = 49
		line_und  = ['_']*(int(columns))
		line_u    = ''.join(map(str, line_und))
		line_u    = colored(line_u, 'magenta', attrs=['bold'])
		line_hint = ['_']*(int(columns)-14)
		line_h    = ''.join(map(str, line_hint))

		#print(x_row+' x '+y_columns)

		curdate = datetime.datetime.now()
		getdate = curdate.strftime('%A, %d %B %Y')
		gettime = curdate.strftime('%I:%M:%S %p')
		print(colored(' _______ _______ _______ ___ ___  ___ _______', 'cyan', attrs=['bold']) , colored('__                __       ', 'yellow', attrs=['bold']))
		print(colored('|   _   |   _   |   _   |   Y   )|   |   _  ', 'cyan', attrs=['bold']) , colored('|  |--.---.-.-----|__.----.', 'yellow', attrs=['bold']))
		print(colored('|.  1___|.  |   |.  |   |.  1  / |.  |. ____', 'cyan', attrs=['bold']),  colored('|  _  |  _  |__ --|  |  __|', 'yellow', attrs=['bold']))
		print(colored('|.  |___|.  |   |.  |   |.  _  \ |.  |. ____', 'cyan' , attrs=['bold']), colored('|_____|___._|_____|__|____|', 'yellow', attrs=['bold']))
		print(colored('|:  1   |:  1   |:  1   |:  |   \|:  |:  1   |' , 'cyan' , attrs=['bold']))
		print(colored('|::.. . |::.. . |::.. . |::.| .  |::.|::.. . |  ' , 'cyan' , attrs=['bold']) + colored(str(getdate).upper(), 'cyan', attrs=['bold']))
		print(colored("`-------`-------`-------`--- ---'`---`-------'  ", 'cyan' , attrs=['bold']) + colored(str(gettime).upper(), 'yellow', attrs=['bold']))
		print(line_u)
		print(line_u+'\n')

	def clr(self, letter, color):
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

	def m_clr(self, title, text):
		menu = self.clr('[','y')+self.clr(title,'c')+self.clr(']','y')+' '+text
		return menu

	def menu_display(self):
		#row, columns = os.popen('stty size', 'r').read().split()
		columns  = 109
		rows     = 49
		line_und = ['_']*(int(columns))
		line_u   = ''.join(map(str, line_und))
		line_u   = colored(line_u, 'magenta', attrs=['bold'])

		print('|::     '+self.m_clr('NS','NETWORK SCANNER')+'  |  '+self.m_clr('PS','PORT SCANNER')+'  |  '+self.m_clr('SF','SUBNET FINDER')+'     |  '+self.m_clr('ZC','ZIP PASS-CRACKER')+'    ::|')
		print('|::     '+self.m_clr('DF','DATA-GEN FAKER')+'   |  '+self.m_clr('MB','MAIL BOMBER')+'   |  '+self.m_clr('RO','CIPHER-GEN ROT13')+'  |  '+self.m_clr('SB','SSH BRUTEFORCE')+'      ::|')
		print('|::     '+self.m_clr('RS','CIPHER-GEN RSA')+'   |  '+self.m_clr('WS','WEB SCRAPPER')+'  |  '+self.m_clr('ZD','ZIP OF DEATH')+'      |  '+self.m_clr('SS','SHODAN SEEKER')+'       ::|')
		print('|::     '+self.clr('----------------------------------------------------------------------------------------------','m')+'    ::|')
		print('|::     '+self.clr('OPTION','c')+' : '+self.clr('[clear] // [menu] // [home] // [exit] // [help]','y')+'                                          ::|')
		print(line_u+'\n')

	def menu_display_input(self):
		#ows, columns = os.popen('stty size', 'r').read().split()
		rows    = 49
		columns = 109
		if (int(columns) >= 109) and (int(rows) >= 49):
			menu_input = input(colored('>> ', 'yellow', attrs=['bold']))
			return menu_input
		else:
			print("\n"+clr('Info:','y')+" please consider to resize your terminal screen into atleast ["+clr('49','c')+' x '+clr('109','c')+"] characters")
			print('      your current resosultion are [%s x %s] characters, which may cause some results' % (clr(rows,'c'), clr(columns,'c')))
			print('      not in a proper and desired format ...\n      Program exiting now :( \n')
			sys.exit(0)

	def sw_case_menu(self, key):
		#row, columns = os.popen('stty size', 'r').read().split()
		bug_logger = BugLogger()
		cipher_r13 = CipherROT13()
		net_scan   = NetworkScanner()
		port_scan  = PortScanner()
		sub_finder = SubnetFinder()
		data_faker = DataFaker()
		mail_bomb  = MailBomber()
		cipher_rsa = CipherRSA()

		rows      = 49
		columns   = 109
		line_und  = ['_']*(int(columns))
		line_u    = ''.join(map(str, line_und))
		line_u    = colored(line_u, 'magenta', attrs=['bold'])
		checker = 'false'
		if key == 'clear':
			clear()
		elif key == 'home':
			clear()
			self.main_method()
		elif key == 'menu':
			print(line_u+'\n')
			self.menu_display()
		elif key == 'exit':
			sys.exit(0)
		elif key == 'NS':
			print(line_u+'\n')
			net_scan.network_scan_proc(net_scan.network_scan_input())
			print(line_u+'\n')
		elif key == 'PS':
			print(line_u+'\n')
			port_scan.port_scan_proc(port_scan.port_scan_input())
			print(line_u+'\n')
		elif key == 'SF':
			print(line_u+'\n')
			sub_finder.subnet_finder_proc()
			print(line_u+'\n')
		elif re.search('DF', key):
			print(line_u+'\n')
			data_faker.data_gen_proc(key)
			print(line_u+'\n')
		elif key == 'MB':
			print(line_u+'\n')
			mail_bomb.mail_bomber_proc()
			print(line_u+'\n')
		elif key == 'RO':
			print(line_u+'\n')
			cipher_r13.cipher_gen_rot13_proc()
			print(line_u+'\n')
		elif key == 'RS':
			print(line_u+'\n')
			cipher_rsa.cipher_gen_rsa_proc()
			print(line_u+'\n')

	def main_method(self):
		checker = 'false'
		self.header()
		self.menu_display()
		while checker == 'false':
			key = self.menu_display_input()
			self.sw_case_menu(key)

if __name__ == "__main__":
	obj = CookieBasic()
	#os.chdir('cookie-basic')
	while 1 > 0:
		#rows, columns = os.popen('stty size', 'r').read().split()
		dir_manda = ['log','cipher','conf','container','sandbox','test-repos','wordlist-master']
		dir_check = [None]*len(dir_manda)
		dir_fin   = True
		for i in range(len(dir_manda)):
			dir_check[i] = path.exists(dir_manda[i])
			if dir_check[i] == False:
				#print(dir_manda[i])
				dir_fin = False
				break
		if dir_fin == True:
			rows = 49
			columns = 109
			if (int(columns) >= 109) and (int(rows) >= 49):
				obj.main_method()
			else:
				print("\n"+obj.clr('Info:','y')+" please consider to resize your terminal screen into atleast ["+obj.clr('49','c')+' x '+obj.clr('109','c')+"] characters")
				print('      your current resosultion are [%s x %s] characters, which may cause some results' % (obj.clr(rows,'c'), obj.clr(columns,'c')))
				print('      not in a proper and desired format ...\n      Program exiting now :( \n')
				sys.exit(0)
		else:
			print('\n'+obj.clr('Info:','y')+" program detects that user did not run it on %s" % obj.clr('cookie-basic root directory','g'))
			print('      this prevention will avoid any mislocate files or directory for I/O process in the future')
			print('      please consider to run this in a proper directory ...\n      Program exiting now :( \n')
			print(str(os.getcwd()))
			sys.exit(0)

