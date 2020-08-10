import nmap
import time
import datetime
import re
import os

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
        curdate = datetime.datetime.now()
        fldate   = curdate.strftime('%d-%m-%Y')
        gettime  = curdate.strftime('%I:%M:%S %p')
        str_time = fldate+' '+gettime
        try:
            logs = open(str(os.getcwd())+'/log/nmap/'+fldate+'.ps.log', "a+")
            nmap_sc.scan(host, arguments='-O -sV -T4')
            port_list = len(nmap_sc[host]['tcp'].keys())
            info_host = 'Host\t: %s (%s)' % (nmap_sc[host].hostname(), host)
            info_mchn = 'Machine\t: %s %s (%s)' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['osfamily'], nmap_sc[host]['osmatch'][0]['osclass'][0]['osgen'],nmap_sc[host]['osmatch'][0]['osclass'][0]['vendor'])
            info_krnl = 'Kernel\t: %s' % (nmap_sc[host]['osmatch'][0]['osclass'][0]['cpe'])
            print(info_host+'\n'+info_mchn+'\n'+info_krnl)
            logs.write('______________________\n'+str_time+'\n----------------------\n')
            logs.write(info_host+'\n'+info_mchn+'\n'+info_krnl+'\n')
            try:
                print('Ports\t: %s ports are open, %s not shown\n' % (port_list, str((1000-port_list))))
                logs.write('Ports\t: %s ports are open, %s not shown\n' % (port_list, str((1000-port_list))))
                print('   PORTS   STAT\t SERVICE\t  VERSION DETAIL')
                logs.write('   PORTS   STAT\t SERVICE\t  VERSION DETAIL\n')
                print('   -----   ----\t -------\t  --------------')
                logs.write('   -----   ----\t -------\t  --------------\n')
                for ports in nmap_sc[host]['tcp'].keys():
                    fm_ports = '{:<6}'.format(ports)
                    product_detail = '{:<14}'.format((str(nmap_sc[host]['tcp'][ports]['name']).upper() + ' ' + str(nmap_sc[host]['tcp'][ports]['version']))[:13])
                    version_detail = '{:<6}'.format((nmap_sc[host]['tcp'][ports]['product'] + ' ' + nmap_sc[host]['tcp'][ports]['extrainfo'])[:38])
                    state_detail   = '{:<3}'.format(str(nmap_sc[host]['tcp'][ports]['state']).upper()[:4])
                    print('|- %s  %s\t %s | %s' % (fm_ports, state_detail, product_detail, version_detail))
                    logs.write('|- %s  %s\t %s | %s\n' % (fm_ports, state_detail, product_detail, version_detail))
                frmt_query = '{:.3f}'.format(time.time() - go_time)
                logs.write('\n')
                logs.close()

                print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
            except:
                curdate = datetime.datetime.now()
                fldate  = curdate.strftime('%m-%Y')
                print('Host requires atleast 1 open port for the scanning, therefore please check the IP formatting')
                print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
                bug_logger.bug_logger_proc('PS')
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('Host requires atleast 1 open port for the scanning, therefore please check the IP formatting')
            print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('PS')
