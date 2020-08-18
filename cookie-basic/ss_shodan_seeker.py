import mmh3
import shodan
import requests
import os
import json
import codecs
import sys
import re
import time
import datetime

from termcolor import colored
from bug_logger import BugLogger

class ShodanSeeker:

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

	def get_shodankey(self):
		bug_logger = BugLogger()
		try:
			with open(str(os.getcwd())+"/conf/shodan_api.json","r") as f:
				shodan_api = json.load(f)
			for key in shodan_api:
				get_key = key['api-key']
			return get_key
		except:
			curdate = datetime.datetime.now()
			fldate  = curdate.strftime('%m-%Y')
			print('\nVerify and confirm your key of the Shodan API with your account in '+self.clr('conf/shodan_api.json','g'))
			print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
			bug_logger.bug_logger_proc('SS')

	def shodan_hash(self, param):
		try:
			response = requests.get(param, verify=False)
			favicon  = codecs.encode(response.content, 'base64')
			hash = mmh3.hash(favicon)
			#print('\nShodan favicon hasher : %s' % hash)
			return "["+str(hash)+"]"
		except:
			return ""

	def shodan_search(self, target, target_hash, go_time):
		bug_logger = BugLogger()		
		curdate = datetime.datetime.now()
		fldate   = curdate.strftime('%d-%m-%Y')		
		gettime  = curdate.strftime('%I:%M:%S %p')
		str_time = fldate+' '+gettime		
		columns  = 109
		rows     = 49
		line_und = ['-']*(int(columns))
		line_u   = ''.join(map(str, line_und))
		line_u   = colored(line_u, 'cyan', attrs=['bold'])		
		try:
			get_key = self.get_shodankey()
			api = shodan.Shodan(get_key)
			deg = u"\N{DEGREE SIGN}"
			dnsResolve = 'https://api.shodan.io/dns/resolve?hostnames='+target+'&key='+get_key

			resolved = requests.get(dnsResolve)
			hostIP = resolved.json()[target]

			host    = api.host(hostIP, history=False)
			result  = api.host(host['ip_str'])
			port_countr = 0
			vuln_countr = 0
			tech_countr = 0
			tech_check  = False

			str_target = ""
			arr_target = re.split('; |, |\.', target)
			for i in arr_target:
				str_target += i
			#print (str_target)
			#pnjacid.10-08-2020.shodan.log						
			logs = open(str(os.getcwd())+'/log/shodan/'+str_target+'.'+fldate+'.shodan.log', "w+")
			logs.write('______________________\n'+str_time+'\n----------------------\n')			
			logs.write("Target domain   : "+target+'\n')
			try:
				for item in host['data']:
					port_countr += 1
			except:
				abstract_ass = None
			try:
				for item in host['data'][0]['vulns']:
					vuln_countr += 1
			except:
				abstract_ass = None
			for i in range(10):
				try:
					for item in host['data'][i]['http']['components']:
						tech_countr += 1
						tech_check = True
					if tech_check:
						break
				except:
					abstract_ass = None

			tech_check  = False
			for i in range(10):
				try:
					print ("\n"+line_u+"\n"+self.clr('Domain Profile','g')+"\n"+line_u)
					print ("Profile hash    : %s" % target_hash)
					print ("IP address      : %s" % host['ip_str'])
					print ("AS number       : %s" % host['asn'])
					print ("Domain regist   : %s" % host['domains'])					
					print ("Organization    : %s" % host['org'])
					print ("ISP source      : %s" % host['isp'])
					logs.write('-----------------\nDomain Profile\n-----------------\n')
					logs.write("Profile hash    : %s\n" % target_hash)
					logs.write("IP address      : %s\n" % host['ip_str'])
					logs.write("AS number       : %s\n" % host['asn'])
					logs.write("Domain regist   : %s\n" % host['domains'])					
					logs.write("Organization    : %s\n" % host['org'])
					logs.write("IS provider     : %s\n" % host['isp'])		
					break
					## sampai disini			
				except:
					abstract_ass = None

			city_check = False
			try:
				for i in range(10):
					try:
						print ("Origin domain   : %s, %s (%s)" % (host['data'][i]['ssl']['cert']['subject']['ST'], host['country_name'], host['country_code']))
						logs.write("Origin domain   : %s, %s (%s)\n" % (host['data'][i]['ssl']['cert']['subject']['ST'], host['country_name'], host['country_code']))						
						city_check = True						
					except:
						abstract_ass = None
				if city_check == False:
					print ("Origin domain   : %s (%s)" % (host['country_name'], host['country_code']))
					logs.write("Origin domain   : %s (%s)\n" % (host['country_name'], host['country_code']))																
				print ("Origin coordnt  : %s x %s" % (str(host['longitude'])+deg, str(host['latitude'])+deg))					
				logs.write("Origin coordnt  : %s x %s\n" % (str(host['longitude'])+deg, str(host['latitude'])+deg))									
			except:
				abstract_ass = None

			for i in range(10):
				try:
					print ("| - Timestamp   : %s (%s)" % (host['data'][i]['timestamp'],host['data'][i]['port']))					
					logs.write("| - Timestamp   : %s (%s)\n" % (host['data'][i]['timestamp'],host['data'][i]['port']))										
				except:
					abstract_ass = None

			print (line_u+"\n"+self.clr('Technologies    : [ '+str(tech_countr)+' ]','g')+"\n"+line_u)
			logs.write('-----------------\nTechnologies\n-----------------\n')			
			for i in range(10):
				try:
					backend = "Backend Infras  : " + str(host['data'][i]['info'])
					print (backend)
					logs.write(backend+'\n')
					break
				except:
					abstract_ass = None
			for i in range(10):
				try:
					for item in host['data'][i]['http']['components']:
						print ("| - %s (%s)" % (item, host['data'][i]['http']['components'][item]['categories']))
						logs.write("| - %s (%s)\n" % (item, host['data'][i]['http']['components'][item]['categories']))						
						tech_check = True
					if tech_check:
						break
				except:
					abstract_ass = None
			logs.close()
			##sampai sini
			try:
				print (line_u+"\n"+self.clr('Open Services   : [ '+str(port_countr)+' ]','g')+"\n"+line_u)
				port_det = ""
				for item in host['data']:
					try:
						print ("Open Port\t: %s/%s (%s %s)" % (item['port'],str(item['transport']).upper(),item['product'],item['version']))
					except:
						try:
							print ("Open Port\t: %s/%s (%s)" % (item['port'],str(item['transport']).upper(),item['product']))
						except:
							try:
								print ("Open Port\t: %s/%s" % (item['port'],str(item['transport']).upper()))
							except:
								abstract_ass = None
					try:
						try:
							print ("| - Fingerprint\t: %s in %s" % (item['ssl']['dhparams']['fingerprint'], item['ssl']['dhparams']['bits']))
						except:
							abstract_ass = None
						for ssl_ver in item['ssl']['versions']:
							port_det += str(ssl_ver) + " / "
						print ("| - SSL Vers\t: %s" % port_det)							
						try:
							print ("| - Cipher-Algo\t: %s in %s bit" % (item['ssl']['cipher']['name'], item['ssl']['cipher']['bits']))
						except:
							abstract_ass = None
						print ("| - Signtr-Algo\t: %s ver %s modulus %s bit" % (item['ssl']['cert']['sig_alg'],item['ssl']['cert']['version'],item['ssl']['cert']['pubkey']['bits']))
						try:
							print ("| - Subj-Issuer\t: %s, %s (%s)" % (item['ssl']['cert']['subject']['OU'],item['ssl']['cert']['subject']['O'], host['country_code']))
						except:	
							abstract_ass = None							
						print ("| - Cert-Issuer\t: %s, %s (%s)" % (item['ssl']['cert']['issuer']['O'], item['ssl']['cert']['issuer']['CN'], item['ssl']['cert']['issuer']['C']))
					except:
						abstract_ass = None
			except:
				abstract_ass = None

			for i in host['data']:
				try:
					banner = i['data']
					banner = banner.strip()
					str_banner = str(banner)
					if banner != "":
						print (line_u+"\n"+self.clr('Banner Services : [ '+str(i['port'])+'/'+str(i['transport']).upper()+' ]','g')+"\n"+line_u)
						print (str_banner)
				except:
					abstract_ass = None

			try:
				end_line = False
				parag = True
				print (line_u+"\n"+self.clr('Vulnerabilities : [ '+str(vuln_countr)+' ]','g')+"\n"+line_u)
				for item in host['data'][0]['vulns']:
					if parag:
						print ('| - [%s/10.0] %s' % (host['data'][0]['vulns'][item]['cvss'], item), end="")
						parag = False
						end_line = False
						continue
					else:
						print ('\t| - [%s/10.0] %s' % (host['data'][0]['vulns'][item]['cvss'], item))
						parag = True
						end_line = True
						continue
				if end_line == False:
					print ("")
			except:
				abstract_ass = None
			frmt_query = '{:.3f}'.format(time.time() - go_time)
			print(self.clr('\nQuery finished successfully in','y')+' %s seconds ...' % (frmt_query))				
		except:
			curdate = datetime.datetime.now()
			fldate  = curdate.strftime('%m-%Y')
			print('\nVerify the domain name or the IP public is currently exists, along with the correct format')
			print('Also confirm your API key of the Shodan API with your account in '+self.clr('conf/shodan_api.json','g'))			
			print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
			bug_logger.bug_logger_proc('SS')

	def shodan_seeker_proc(self):
		bug_logger = BugLogger()
		target = input(self.clr("Target domain\t: ",'c'))
		passer_hash = ""
		go_time = time.time()
		try:
			print ("Initiate shodan API query for %s ..." % target)
			try:
				target_hash = "https://"+target+"/"
				passer_hash = self.shodan_hash(target_hash)
			except:
				try:
					target_hash = "http://"+target+"/"
					passer_hash = self.shodan_hash(target_hash)				
				except:
					passer_hash = ""
			self.shodan_search(target, passer_hash, go_time)
		except:
			abstract_ass = None

## main
#obj = ShodanSeeker()
#obj.shodan_seeker_proc()
