import time
import datetime
import re

from termcolor import colored
from bug_logger import BugLogger

class SubnetFinder:

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

    def subnet_finder_proc(self):
        bug_logger = BugLogger()
        try:
            netmask = [255, 255, 255, 255]
            default = [0, 0, 0, 0]
            ip = input(self.clr("IP Address / Prefix\t: ",'c'))
            host = int(input(self.clr("Total Required Hosts\t: ",'c')))
            go_time = time.time()

            # section 1
            calculated_prefix = 0
            power_user_prefix = 0
            calculated_class = 'A'
            increment_prefix = 2
            increment_square = 0
            increment_square2 = 0
            increment_basic = 0
            new_prefix = 0
            next_inc_bit = 0
            next_limit_bit = 0
            arr_user_ip = re.split('; |, |\.|\/', ip)
            class_char = ['A', 'B', 'C', 'D']
            class_range = [0, 128, 192, 224]
            class_deter = int(arr_user_ip[0])
            thirdbit_deter = 0

            while host > 0:
                if host <= (increment_prefix - 2):
                    break
                increment_prefix *= 2
                increment_square += 1
            increment_square += 1
            calculated_prefix = 32 - increment_square
            total_host = pow(2, increment_square)
            power_user_prefix = pow(2, (32-int(arr_user_ip[4])))

            for a in range(len(class_char)):
                if class_deter < class_range[a]:
                    break
                calculated_class = class_char[a]

            print('\nCIDR Prefix\t\t: /%s - %s host' % (calculated_prefix, total_host))
            print('Subnet Class\t\t: %s \n' % calculated_class)

            # section 2
            if (int(arr_user_ip[3]) / increment_prefix) < 1:
                arr_user_ip[3] = '0'
            else:
                thirdbit_deter = int(arr_user_ip[3]) / increment_prefix
                if thirdbit_deter > 1:
                    while int(arr_user_ip[3]) > total_host:
                        if int(arr_user_ip[3]) < increment_square2:
                            break
                        increment_square2 += total_host
                    increment_square2 -= total_host
                    arr_user_ip[3] = increment_square2

            na_ip_octet = [0]*4
            fua_ip_octet = [0]*4
            lua_ip_octet = [0]*4
            ba_ip_octet = [0]*4

            for i in range(len(na_ip_octet)):
                na_ip_octet[i] = int(arr_user_ip[i])
                fua_ip_octet[i] = int(arr_user_ip[i])
                lua_ip_octet[i] = int(arr_user_ip[i])
                ba_ip_octet[i] = int(arr_user_ip[i])

            fua_ip_octet[3] += 1
            lua_ip_octet[3] = (na_ip_octet[3] + total_host) - 2
            ba_ip_octet[3] = (na_ip_octet[3] + total_host) - 1

            if lua_ip_octet[3] > 254:
                increment_basic = (lua_ip_octet[3]+2) - 256
                next_inc_bit = int(increment_basic/256)
                lua_ip_octet[2] += next_inc_bit
                ba_ip_octet[2] += next_inc_bit
                lua_ip_octet[3] = 254
                ba_ip_octet[3] = 255

            if lua_ip_octet[2] > 255:
                next_limit_bit = 256 - int(total_host/256)
                na_ip_octet[2] = next_limit_bit
                fua_ip_octet[2] = next_limit_bit
                lua_ip_octet[2] = 255
                ba_ip_octet[2] = 255

            print('Network Address\t\t: %s.%s.%s.%s/%s' % (na_ip_octet[0], na_ip_octet[1], na_ip_octet[2], na_ip_octet[3], calculated_prefix))
            print('First Usable Address\t: %s.%s.%s.%s/%s' % (fua_ip_octet[0], fua_ip_octet[1], fua_ip_octet[2], fua_ip_octet[3], calculated_prefix))
            print('Last Usable Address\t: %s.%s.%s.%s/%s' % (lua_ip_octet[0], lua_ip_octet[1], lua_ip_octet[2], lua_ip_octet[3], calculated_prefix))
            print('Broadcast Address\t: %s.%s.%s.%s/%s' % (ba_ip_octet[0], ba_ip_octet[1], ba_ip_octet[2], ba_ip_octet[3], calculated_prefix))

            allocated_host = total_host - 2
            efficiency = [int((host/allocated_host) * 100), (allocated_host-host)]
            poss_network = int(power_user_prefix/total_host)

            print('\nAllocated Host\t\t: %s host out of %s available per subnet' % (host, allocated_host))
            print('Efficiency Meter\t: %s%% - %s wasted per subnet' % (efficiency[0], efficiency[1]))
            print('Possible Network\t: %s block space\n' % poss_network)

            template_subnetmask = [8, 8, 8, 8]
            catch_subnetmask = [0, 0, 0, 0]
            new_subnetmask = [0, 0, 0, 0]
            new_subnetmask_bin = [0, 0, 0, 0]
            new_wildcard = [255, 255, 255, 255]
            new_wildcard_bin = [0, 0, 0, 0]
            catch_prefix = calculated_prefix

            for i in range(len(template_subnetmask)):
                if catch_prefix >= template_subnetmask[i]:
                    catch_subnetmask[i] = template_subnetmask[i]
                    catch_prefix -= template_subnetmask[i]
                else:
                    catch_subnetmask[i] = catch_prefix
                    break

            for i in range(len(catch_subnetmask)):
                new_subnetmask[i] = 256 - (pow(2, (8-catch_subnetmask[i])))
                new_wildcard[i] -= new_subnetmask[i]
                new_subnetmask_bin[i] = '{:08b}'.format(new_subnetmask[i])
                new_wildcard_bin[i] = '{:08b}'.format(new_wildcard[i])

            print('Subnet Mask\t\t: %s.%s.%s.%s' % (new_subnetmask[0], new_subnetmask[1], new_subnetmask[2], new_subnetmask[3]))
            print('8-bit notation\t\t: %s.%s' % (new_subnetmask_bin[0], new_subnetmask_bin[1]))
            print('\t\t\t  %s.%s' % (new_subnetmask_bin[2], new_subnetmask_bin[3]))
            print('Wildcard Mask\t\t: %s.%s.%s.%s' % (new_wildcard[0], new_wildcard[1], new_wildcard[2], new_wildcard[3]))
            print('8-bit notation\t\t: %s.%s' % (new_wildcard_bin[0], new_wildcard_bin[1]))
            print('\t\t\t  %s.%s' % (new_wildcard_bin[2], new_wildcard_bin[3]))
            frmt_query = '{:.3f}'.format(time.time() - go_time)
            print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print('\nIP Address requires the prefix to be included, therefore please check the IP formatting')
            print('Check out '+self.clr('log/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('SF')
