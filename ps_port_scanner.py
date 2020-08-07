import nmap
import time
import datetime
import re

from termcolor import colored
from bug_logger import BugLogger

class PortScanner:

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

    def port_scan_input(self):
        host = input(self.clr('Target IP Address : ','c'))
        print('Initiate port scanning for (%s) ...\n' % host)
        return host

    def port_scan_proc(self, host):
        go_time = time.time()
        nmap_sc = nmap.PortScanner()
        bug_logger = BugLogger()
        try:
            nmap_sc.scan(host, arguments='-O -sV -T4')
            port_list = len(nmap_sc[host]['tcp'].keys())
            print('Host\t: %s (%s)' % (nmap_sc[host].hostname(), host))
            print('Machine\t: %s %s (%s)' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['osfamily'], nmap_sc[host]['osmatch'][0]['osclass'][0]['osgen'],nmap_sc[host]['osmatch'][0]['osclass'][0]['vendor']))
            print('Kernel\t: %s' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['cpe']))
            try:
                print('Ports\t: %s ports are open, %s not shown\n' % (port_list, str((1000-port_list))))
                print('   PORTS   STAT\t SERVICE\t  VERSION DETAIL')
                print('   -----   ----\t -------\t  --------------')
                for ports in nmap_sc[host]['tcp'].keys():
                    fm_ports = '{:<6}'.format(ports)
                    product_detail = '{:<14}'.format((str(nmap_sc[host]['tcp'][ports]['name']).upper() + ' ' + str(nmap_sc[host]['tcp'][ports]['version']))[:13])
                    version_detail = '{:<6}'.format((nmap_sc[host]['tcp'][ports]['product'] + ' ' + nmap_sc[host]['tcp'][ports]['extrainfo'])[:38])
                    state_detail   = '{:<3}'.format(str(nmap_sc[host]['tcp'][ports]['state']).upper()[:4])
                    print('|- %s  %s\t %s | %s' % (fm_ports, state_detail, product_detail, version_detail))
                frmt_query = '{:.3f}'.format(time.time() - go_time)
                print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
            except:
                curdate = datetime.datetime.now()
                fldate  = curdate.strftime('%m-%Y')
                print('Host requires atleast 1 open port for the scanning, therefore please check the IP formatting')
                print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
                bug_logger.bug_logger_proc('PS')
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('Host requires atleast 1 open port for the scanning, therefore please check the IP formatting')
            print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('PS')
