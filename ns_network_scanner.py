import nmap
import time
import re

from termcolor import colored
from bug_logger import BugLogger

class NetworkScanner:

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

    def network_scan_input(self):
        network = input(self.clr('Network range and prefix : ','c'))
        print('Initiate network scanning for (%s) ...\n' % network)
        return network

    def network_scan_proc(self, network):
        go_time = time.time()
        nmap_sc = nmap.PortScanner()
        bug_logger = BugLogger()
        try:
            nmap_sc.scan(network, arguments='-T5')
            net_prefix = re.split('; |, |\/', network)
            total_prefix = 32 - int(net_prefix[1])
            total_host = pow(2, total_prefix)
            print('Successfully collected %s active hosts out of %s \n' % (len(nmap_sc.all_hosts()), total_host))
            for host in nmap_sc.all_hosts():
                print('|- %s (%s)' % (host, nmap_sc[host].hostname()))
            frmt_query = '{:.3f}'.format(time.time() - go_time)
            print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
        except:
            print('Network range requires the prefix to be included in correct format')
            print('Check out '+self.clr('bug-tracker.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('NS')
