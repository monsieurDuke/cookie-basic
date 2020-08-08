import nmap
import time
import datetime
import re
import pytest

from termcolor import colored
from test_bug_logger import TestBugLogger

class TestNetworkScanner:

    @pytest.fixture
    def test_clr(self, letter, color):
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

    def test_network_scan_input(self):
        network = '192.168.1.0/24'
        print('Initiate network scanning for (%s) ...\n' % network)
        return network

    @pytest.fixture
    def test_network_scan_proc(self, network):
        go_time = time.time()
        nmap_sc = nmap.PortScanner()
        bug_logger = TestBugLogger()
        try:
            nmap_sc.scan(network, arguments='-T5')
            net_prefix = re.split('; |, |\/', network)
            total_prefix = 32 - int(net_prefix[1])
            total_host = pow(2, total_prefix)
            print('Successfully collected %s active hosts out of %s \n' % (len(nmap_sc.all_hosts()), total_host))
            for host in nmap_sc.all_hosts():
                print('|- %s (%s)' % (host, nmap_sc[host].hostname()))
            frmt_query = '{:.3f}'.format(time.time() - go_time)
            print('\n'+self.test_clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('Network range requires the prefix to be included in correct format')
            print('Check out '+self.test_clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.test_bug_logger_proc('NS')
