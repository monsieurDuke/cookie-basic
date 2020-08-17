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
		with open(str(os.getcwd())+"/../conf/shodan_api.json","r") as f:
			shodan_api = json.load(f)
		for key in shodan_api:
			get_key = key['api-key']
		return get_key

	def shodan_hash(self, param):
		response = requests.get(param, verify=False)
		favicon  = codecs.encode(response.content, 'base64')
		hash = mmh3.hash(favicon)
		print('\nShodan favicon hasher : %s' % hash)

	def shodan_search(self, target):
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
				print ("\n------------------------------------------------------------------------------\nDomain Profile\n------------------------------------------------------------------------------")
				print ("IP address      : %s" % host['ip_str'])
				print ("AS number       : %s" % host['asn'])
				print ("Organization    : %s" % host['org'])
				print ("Domain regist   : %s" % host['domains'])
				break
			except:
				abstract_ass = None
		for i in range(10):
			try:
				print ("Origin domain   : %s, %s (%s)" % (host['data'][i]['ssl']['cert']['subject']['ST'],host['country_name'], host['country_code']))
				print ("Origin coordnt  : %s x %s" % (str(host['longitude'])+deg, str(host['latitude'])+deg))
				print ("Last timestamp  : %s" % host['data'][i]['timestamp'])
				break
			except:
				abstract_ass = None

		print ("------------------------------------------------------------------------------\nTechnologies    : [ %s ]\n------------------------------------------------------------------------------" % tech_countr)
		for i in range(10):
			try:
				backend = "Backend Infras  : " + str(host['data'][i]['info'])
				print (backend)
				break
			except:
				abstract_ass = None
		for i in range(10):
			try:
				for item in host['data'][i]['http']['components']:
					print ("| - %s (%s)" % (item, host['data'][i]['http']['components'][item]['categories']))
					tech_check = True
				if tech_check:
					break
			except:
				abstract_ass = None

		try:
			print ("------------------------------------------------------------------------------\nOpen Services   : [ %s ]\n------------------------------------------------------------------------------" % port_countr)
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
					print ("| - Signtr-Algo\t: %s ver %s modulus %s bit" % (item['ssl']['cert']['sig_alg'],item['ssl']['cert']['version'],item['ssl']['cert']['pubkey']['bits']))
					print ("| - Subj-Issuer\t: %s, %s (%s)" % (item['ssl']['cert']['subject']['OU'],item['ssl']['cert']['subject']['O'], host['country_code']))
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
					print ("------------------------------------------------------------------------------\nBanner Services : [ %s/%s ]\n------------------------------------------------------------------------------" % (i['port'], str(i['transport']).upper()))
					print (str_banner)
			except:
				abstract_ass = None

		try:
			end_line = False
			parag = True
			print ("------------------------------------------------------------------------------\nVulnerabilities : [ %s ]\n------------------------------------------------------------------------------" % vuln_countr)
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

	def shodan_seeker_proc(self):
		bug_logger = BugLogger()
		target = input(self.clr("Target domain\t: ",'c'))
		try:
			print ("Initiate shodan API query for %s ..." % target)
			self.shodan_hash(target)
			self.shodan_search(target)
		except:
			bug_logger.bug_logger_proc('SS')

## main
obj = ShodanSeeker()
obj.shodan_seeker_proc()
