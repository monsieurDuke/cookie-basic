import mmh3
import shodan
import requests
import os
import json
import codecs
import sys
import re

class ShodanSeeker:

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

		for item in host['data']:
			port_countr += 1
		for item in host['data'][0]['vulns']:
			vuln_countr += 1
		for item in host['data'][0]['http']['components']:
			tech_countr += 1
		try:
			print ("\n------------------------------------------------------------------------------\nDomain Profile\n------------------------------------------------------------------------------")
			print ("Favicon hasher\t: http.favicon.hash:%s" % host['data'][0]['hash'])
			print ("Hostname        : %s" % host['data'][0]['http']['host'])
			print ("IP address      : %s" % host['ip_str'])
			print ("AS Number       : %s" % host['asn'])
			print ("Organization    : %s" % host['org'])
			try:
				print ("Hostname rgst   : %s" % host['domains'][0])
			except:
				abstract_ass = None
			print ("Origin domain   : %s, %s (%s)" % (host['data'][0]['ssl']['cert']['subject']['ST'],host['country_name'], host['country_code']))
			print ("Origin coordnt  : %s x %s" % (str(host['data'][0]['location']['longitude'])+deg, str(host['data'][0]['location']['latitude'])+deg))
			print ("Last timestamp  : %s" % host['data'][0]['timestamp'])
		except:
			abstract_ass = None

		print ("------------------------------------------------------------------------------\nTechnologies    [ %s ]\n------------------------------------------------------------------------------" % tech_countr)
		print ("Backend Infras  : %s" % host['data'][0]['info'])
		for item in host['data'][0]['http']['components']:
			print ("| - %s (%s)" % (item, host['data'][0]['http']['components'][item]['categories'][0]))

		print ("------------------------------------------------------------------------------\nOpen Services   [ %s ]\n------------------------------------------------------------------------------" % port_countr)
		for item in host['data']:
			print ("Open Port\t: %s/%s" % (item['port'],str(item['transport']).upper()))
			try:
				print ("Service\t\t: %s %s" % (item['product'],item['version']))
			except:
				abstract_ass = None
			try:
				print ("Fingerprint\t: %s in %s" % (item['ssl']['dhparams']['fingerprint'], item['ssl']['dhparams']['bits']))
				print ("SSL Versions\t: ",end="")
				for ssl_ver in item['ssl']['versions']:
					print (ssl_ver,end=" / ")
				print ("\nSigntr-Algo\t: %s ver %s modulus %s bit" % (item['ssl']['cert']['sig_alg'],item['ssl']['cert']['version'],item['ssl']['cert']['pubkey']['bits']))
				print ("Subj-Issuer\t: %s, %s (%s)" % (item['ssl']['cert']['subject']['OU'],item['ssl']['cert']['subject']['O'], host['country_code']))
				print ("Cert-Issuer\t: %s, %s (%s)\n" % (item['ssl']['cert']['issuer']['O'], item['ssl']['cert']['issuer']['CN'], item['ssl']['cert']['issuer']['C']))
			except:
				abstract_ass = None

		print ("------------------------------------------------------------------------------\nDomain Banner\n------------------------------------------------------------------------------")
#		for i in host['data'][0]['data']:
#			print ('|- %s' % i)
		banner = host['data'][0]['data']
		banner = banner.strip()
		print (banner)

	    # Print vuln information
		parag = True
		print ("------------------------------------------------------------------------------\nVulnerabilities [ %s ]\n------------------------------------------------------------------------------" % vuln_countr)
		for item in host['data'][0]['vulns']:
			if parag:
				print ('| - [%s/10.0] %s' % (host['data'][0]['vulns'][item]['cvss'], item), end="")
				parag = False
				continue
			else:
				print ('\t| - [%s/10.0] %s' % (host['data'][0]['vulns'][item]['cvss'], item))
				parag = True
				continue
#			print ('refs: https://www.cvedetails.com/cve/%s/' % item)

	def shodan_seeker_proc(self):
		target = input("Target domain\t: ")
		print ("Initiate shodan API query for %s ..." % target)
		#self.shodan_hash(target)
		self.shodan_search(target)

## main
obj = ShodanSeeker()
obj.shodan_seeker_proc()
