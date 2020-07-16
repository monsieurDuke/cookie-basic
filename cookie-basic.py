import nmap, datetime, getpass
import sys, time, decimal, re
from clear_screen import clear

nmap_sc = nmap.PortScanner()
curuser = getpass.getuser()

## Main Display
def header():
	clear()
	curdate = datetime.datetime.now()
	getdate = curdate.strftime('%A, %d %b %Y')
	gettime = curdate.strftime('%I:%M:%S %p') + ' | v.1.2.1'
	print('_______ _______ _______ ___ ___  ___ _______ __                __       ')
	print('|   _   |   _   |   _   |   Y   )|   |   _   |  |--.---.-.-----|__.----.')
	print('|.  1___|.  |   |.  |   |.  1  / |.  |.  1___|  _  |  _  |__ --|  |  __|')
	print('|.  |___|.  |   |.  |   |.  _  \ |.  |.  __)_|_____|___._|_____|__|____|')
	print('|:  1   |:  1   |:  1   |:  |   \|:  |:  1   |                          ')
	print('|::.. . |::.. . |::.. . |::.| .  |::.|::.. . |   ' + str(getdate).upper())
	print("`-------`-------`-------`--- ---'`---`-------'   " + str(gettime).upper())
	print('________________________________________________________________________\n')

def menu_display():
	print('::::.   NAVIGATE FOLLOWING MENU OPTIONS TO IT CORRESSPOND NUMBER   .::::')
	print('::::::.__________________________________________________________.::::::\n')
	print('|::    [1] NETWORK SCANNER   [2] PORT SCANNER  [3] SOCKET SCANNER    ::|')
	print('|::    [4] KEY-LOGGER        [5] MAIL BOMBER   [6] LINKDIN HUNTER    ::|')
	print('|::    [7] SSH SHELLSHOCK    [8] BRUTE-FORCE   [M] ...               ::|')
	print('|::    ----------------------------------------------------------    ::|')
	print('|::                  [C] CLEAR SCREEN  &  [E] EXIT                   ::|')
	print('________________________________________________________________________\n')

## User Input
def menu_display_input():
	menu_input = input('>> ')
	return menu_input

def sw_case_menu(key):
	checker = 'false'
	if key == 'C':
		clear()
		main_method()
	elif key == 'E':
		sys.exit(0)
	elif key == '1':
		print('________________________________________________________________________\n')
		network_scan_proc(network_scan_input())
		print('________________________________________________________________________\n')
	elif key == '2':
		print('________________________________________________________________________\n')
		port_scan_proc(port_scan_input())
		print('________________________________________________________________________\n')

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
			print('   PORTS  STAT\t SERVICE\t VERSION DETAIL')
			print('   -----  ----\t -------\t --------------')
			for ports in nmap_sc[host]['tcp'].keys():
				product_detail = '{:<13}'.format((str(nmap_sc[host]['tcp'][ports]['name']).upper() + ' ' + str(nmap_sc[host]['tcp'][ports]['version']))[:13])
				version_detail = '{:<6}'.format((nmap_sc[host]['tcp'][ports]['product'] + ' ' + nmap_sc[host]['tcp'][ports]['extrainfo'])[:38])
				state_detail   = '{:<3}'.format(str(nmap_sc[host]['tcp'][ports]['state']).upper()[:4])
				print('|- %s\t  %s\t %s | %s' % (ports, state_detail, product_detail, version_detail))
			frmt_query = '{:.3f}'.format(time.time() - go_time)
			print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
		except:
			print('It seems that host doesn have any relevant services')
			frmt_query = '{:.3f}'.format(time.time() - go_time)
			print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
	except:
		print('Host requires atleast 1 open port for the scanning')
		print('Also make sure the IP Address is in the correct format')

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

## Main Method
def main_method():
		checker = 'false'
		header()
		menu_display()
		while checker == 'false':
			key = menu_display_input()
			sw_case_menu(key)

while 1 > 0:
	main_method()
