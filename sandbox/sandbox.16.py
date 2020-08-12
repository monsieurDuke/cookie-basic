import mmh3
import shodan
import requests
import os
import json
import codecs
import sys
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
		try:
			# First we need to resolve our targets domain to an IP
			resolved = requests.get(dnsResolve)
			hostIP = resolved.json()[target]

			# Then we need to do a Shodan search on that IP
			host   = api.host(hostIP)
			result = api.host(host['ip_str'])
			print ("IP Address          : %s" % host['ip_str'])
			print ("Organization        : %s" % host['org'])
			print ("Operating System    : %s" % host.get('os', 'n/a'))
			try:
				print ("Hostname Registered : %s" % host['domains'][0])
			except:
				print ("Hostname Registerrd : None")
			print ("Origin Domain       : %s, %s" % (host['country_name'], host['country_code']))
			print ("Origin Location     : %s x %s" % (str(host['data'][0]['location']['longitude'])+deg, str(host['data'][0]['location']['latitude'])+deg))
			print ("Last Timestamp      : %s " % host['data'][0]['timestamp'])
			# Print all banners
			for item in host['data']:
				print ("Port: %s" % item['port'])
				print ("Banner: %s" % item['data'])

		    # Print vuln information
			for item in host['vulns']:
				CVE = item.replace('!','')
				print ('Vulns: %s' % item)
				exploits = api.exploits.search(CVE)
				for item in exploits['matches']:
					if item.get('cve')[0] == CVE:
						print (item.get('description'))
			print (host)
		except:
			error_info = str(sys.exc_info()[1])
			print ('Err: '+error_info)

	def shodan_seeker_proc(self):
		target = input("Target domain : ")
		#self.shodan_hash(target)
		self.shodan_search(target)

## main
obj = ShodanSeeker()
obj.shodan_seeker_proc()
