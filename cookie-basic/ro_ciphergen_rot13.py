import hashlib
import binascii
import re
import time
import datetime
import os

from termcolor import colored
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from bug_logger import BugLogger

class CipherROT13:

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

    def str_to_char(self, text):
        return [char for char in text]

    def cipher_gen_rot13_proc(self):
        bug_logger = BugLogger()
        try:
            file_path =  input(self.clr('FUll path of source : ','c'))
            cipher_act = input(self.clr('Action of cipher    : ','c'))

            file_ext = re.split('; |, |\/', file_path)
            name_file = file_ext[len(file_ext)-1]
            read_plain = open(file_path, 'r')
            plain_str = read_plain.read()
            read_plain.close()

            read_rot13key = open(str(os.getcwd())+'/cipher/.cipher.r13.key', 'r')
            rot13_str = read_rot13key.read()
            read_rot13key.close()

            plain_char = self.str_to_char(plain_str)
            cipher_char = [None]*len(plain_char)
            uncipher_char = [None]*len(cipher_char)
            cipher_str = ''
            uncipher_str = ''
            get_final = ''

            rot13_enc = (self.str_to_char(rot13_str))*2
            count_len = len(rot13_enc)
            rot13_dec = [None]*count_len
            passer = count_len

            check_opt = False

            for i in range(len(rot13_enc)):
                rot13_dec[i] = rot13_enc[passer-1]
                if passer > 0:
                   passer -= 1

            go_time = time.time()

            if cipher_act == 'encrypt':
                get_final = self.rot13_encypt(plain_char, rot13_enc, cipher_char, cipher_str, file_path)
                check_opt = True
            if cipher_act == 'decrypt':
                get_final = self.rot13_decrypt(plain_char, rot13_enc, rot13_dec, uncipher_char, uncipher_str, file_path)
                check_opt = True

            if check_opt:
                frmt_query = '{:.3f}'.format(time.time() - go_time)
                get_result = re.split('; |, |\#', get_final)
                fin_file   = get_result[len(get_result)-1]
                print("\nCipher successfully saved as %s" % self.clr(fin_file,'g'))
                print("Cipher with the "+self.clr('reverse','g')+" extensions means it's in the reverse order")
                print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
            else:
                print("\nThe only valid arguments for the process are "+self.clr("encrypt",'g')+" and "+self.clr("decrypt",'g'))
                print('Please verify what the action needed to do with the source file')
        except:
            curdate = datetime.datetime.now()
            fldate  = curdate.strftime('%m-%Y')
            print("\nPlease verify the source file name and it's path in the correct format")
            print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('RO')

    # encrypting the plain text
    def rot13_encypt(self, plain_char, rot13_enc, cipher_char, cipher_str, file_path):
        try:
            dir_path  = str(os.getcwd())+'/cipher/'
            print('\nDestination path : %s' % dir_path)
            for i in range(len(plain_char)):
                for j in range(len(rot13_enc)):
                    if plain_char[i] == rot13_enc[j]:
                        cipher_char[i] = rot13_enc[j+13]
                        cipher_str += cipher_char[i]
                        break

            file_ext = re.split('; |, |\/', file_path)
            name_file = file_ext[len(file_ext)-1]
            pure_file = name_file+'.encrypt.r13'
            file_path = ''

            if re.search('encrypt', name_file):
                try:
                    get_pure = re.split('; |, |\.encrypt.', name_file)
                    pure_file = get_pure[0]+'.encrypt.r13'
                except:
                    pure_file = get_pure[0]+'.encrypt.r13'
                if re.search('reverse', name_file):
                    pure_file += '.reverse'
            if re.search('decrypt', name_file):
                try:
                    get_pure = re.split('; |, |\.decrypt.', name_file)
                    pure_file = get_pure[0]+'.encrypt.r13'
                except:
                    pure_file = name_file+'.encrypt.r13'
                if re.search('reverse', name_file):
                    pure_file += '.reverse'

            file_path = dir_path+''+pure_file

            print('Destination file : '+pure_file)
            print('Origin file      : '+name_file)
            write_cipher = open(file_path, 'w')
            write_cipher.write(cipher_str)
            write_cipher.close()
            return cipher_str+'#'+pure_file
        except:
            print("It seems program cannot determine the cipher destination path properly")
            print('Please consider to run this program at the root directory of cookie-basic')
            print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('RO')

    # decrypting the plain text
    def rot13_decrypt(self, cipher_char, rot13_enc, rot13_dec, uncipher_char, uncipher_str, file_path):
        try:
            dir_path  = str(os.getcwd())+'/cipher/'
            print('\nDestination path : %s' % dir_path)
            for i in range(len(cipher_char)):
                for j in range(len(rot13_enc)):
                    if cipher_char[i] == rot13_dec[j]:
                        uncipher_char[i] = rot13_dec[j+13]
                        uncipher_str += uncipher_char[i]
                        break

            file_ext = re.split('; |, |\/', file_path)
            name_file = file_ext[len(file_ext)-1]
            pure_file = name_file+'.decrypt.r13.reverse'
            file_path = ''

            if re.search('encrypt', name_file):
                try:
                    get_pure = re.split('; |, |\.encrypt.', name_file)
                    pure_file = get_pure[0]+'.decrypt.r13'
                except:
                    pure_file = name_file+'.decrypt.r13'
            if re.search('decrypt', name_file):
                try:
                    get_pure = re.split('; |, |\.decrypt.', name_file)
                    pure_file = get_pure[0]+'.decrypt.r13'
                except:
                    pure_file = name_file+'.decrypt.r13'
                if re.search('reverse', name_file):
                    pure_file += '.reverse'

            file_path = dir_path+''+pure_file

            print('Destination file : '+pure_file)
            print('Origin file      : '+name_file)
            write_cipher = open(file_path, 'w')
            write_cipher.write(uncipher_str)
            write_cipher.close()
            return uncipher_str+'#'+pure_file
        except:
            print("It seems program cannot determine the cipher destination path properly")
            print('Please consider to run this program at the root directory of cookie-basic')
            print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
            bug_logger.bug_logger_proc('RO')
