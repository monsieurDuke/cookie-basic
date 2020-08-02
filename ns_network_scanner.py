import nmap
import time
import re
from bug_logger import BugLogger

class NetworkScanner:

    def network_scan_input(self):
        network = input('Network range and prefix : ')
        print('Initiate network scanning for (%S) ...\n' % network)
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
            print('\nQuery finished successfully in %s seconds ...' % (frmt_query))
        except:
            print('Network range requires the prefix to be included in correct format')
            print('Check out bug-tracker.log for more detail about this current event')
            bug_logger.bug_logger_proc('NS')
