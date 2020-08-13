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
			host    = api.host(hostIP, history=False)
			result  = api.host(host['ip_str'])
			countr  = 0
			try:
				print ("\n------------------------------------------------------------------------------")
				print ("Favicon hasher\t: http.favicon.hash:%s" % host['data'][0]['hash'])
				print ("IP address      : %s" % host['ip_str'])
				print ("Organization    : %s" % host['org'])
				try:
					print ("Hostname rgst   : %s" % host['domains'][0])
				except:
					print ("Hostname rgst   : None")
				print ("Origin domain   : %s, %s (%s)" % (host['data'][0]['ssl']['cert']['subject']['ST'],host['country_name'], host['country_code']))
				print ("Origin coordnt  : %s x %s" % (str(host['data'][0]['location']['longitude'])+deg, str(host['data'][0]['location']['latitude'])+deg))
				print ("Last timestamp  : %s" % host['data'][0]['timestamp'])
				for item in host['data']:
					countr += 1
				print ("Available Port  : %s" % countr)
			except:
				abstract_ass = None

			# Print all banners
			print ("------------------------------------------------------------------------------")
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
					print ("\nSigntr-Algo\t: %s version %s" % (item['ssl']['cert']['sig_alg'],item['ssl']['cert']['version']))
					print ("Subj-Issuer\t: %s, %s" % (item['ssl']['cert']['subject']['OU'],item['ssl']['cert']['subject']['O']))
#					print ("Banner\t\t: \n%s" % item['data'])
				except:
					abstract_ass = None


		    # Print vuln information
			print ("------------------------------------------------------------------------------")
			for item in host['vulns']:
#				print(host['data'][0])
				try:
					CVE = item.replace('!','')
					print ('vulns: %s\t| https://www.cvedetails.com/cve/%s/' % (item, item))
					exploits = api.exploits.search(CVE)
#					for item in exploits['matches']:
#						if item['cve'][0] == CVE:
				except:
					continue
		except:
			error_info = str(sys.exc_info()[1])
			#print ('Err: '+error_info)

	def shodan_seeker_proc(self):
		target = input("Target domain\t: ")
		print ("Initiate shodan API query for %s ..." % target)
		#self.shodan_hash(target)
		self.shodan_search(target)

## main
obj = ShodanSeeker()
obj.shodan_seeker_proc()
