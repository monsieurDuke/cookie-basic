import zlib
import base64
import os
import datetime
import time
import re

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pathlib import Path
from termcolor import colored
from bug_logger import BugLogger

class CipherRSA:

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

	def generate_new_key_pair(self):
		new_key = RSA.generate(4096, e=65537)
		private_key = new_key.exportKey("PEM")
		public_key = new_key.publickey().exportKey("PEM")

		private_key_path = Path('cipher/.private.pem.rsa.key')
		private_key_path.touch(mode=0o600)
		private_key_path.write_bytes(private_key)

		public_key_path = Path('cipher/.public.pem.rsa.key')
		public_key_path.touch(mode=0o664)
		public_key_path.write_bytes(public_key)

	def encrypt_blob(self, blob, public_key):
		rsa_key = RSA.importKey(public_key)
		rsa_key = PKCS1_OAEP.new(rsa_key)

		blob = zlib.compress(blob)
		chunk_size = 470
		offset = 0
		end_loop = False
		encrypted = bytearray()

		while not end_loop:
			chunk = blob[offset:offset + chunk_size]
			if len(chunk) % chunk_size != 0:
				end_loop = True
				chunk += bytes(chunk_size - len(chunk))
			encrypted += rsa_key.encrypt(chunk)
			offset += chunk_size

		return base64.b64encode(encrypted)

	def decrypt_blob(self, encrypted_blob, private_key):
		rsakey = RSA.importKey(private_key)
		rsakey = PKCS1_OAEP.new(rsakey)

		encrypted_blob = base64.b64decode(encrypted_blob)
		chunk_size = 512
		offset = 0
		decrypted = bytearray()

		while offset < len(encrypted_blob):
			chunk = encrypted_blob[offset: offset + chunk_size]
			decrypted += rsakey.decrypt(chunk)
			offset += chunk_size

		return zlib.decompress(decrypted)

	def cipher_gen_rsa_proc(self):
		bug_logger = BugLogger()
		try:
			new_key    = False
			check_opt  = False
			arg_error  = True
			key_error  = False
			final_file = ''
			file_path  = input(self.clr('Full path of source    : ','c'))
			cipher_act = input(self.clr('Action of cipher       : ','c'))
			dest_path  = str(os.getcwd())+'/cipher/'
			go_time = time.time()

			if cipher_act == 'encrypt':
				check_opt  = True
				arg_error  = False
				key_usage  = input(self.clr('Generate new key (y/n) : ','c'))

				private_key = Path('cipher/.private.pem.rsa.key')
				public_key  = Path('cipher/.public.pem.rsa.key')
				check_file  = open(file_path,'r')
				check_file.close()

				file_ext = re.split('; |, |\/', file_path)
				name_file = file_ext[len(file_ext)-1]
				pure_name = re.split('; |, |\.', name_file)

				unencrypted_file = Path(file_path)
				encrypted_file = unencrypted_file.with_suffix('.'+pure_name[1]+'.encrypt.rsa')

				final_file = name_file+'.encrypt.rsa'
				if key_usage.lower() == 'y':
					self.generate_new_key_pair()
					new_key = True
					key_error = False
				elif key_usage.lower() == 'n':
					new_key = False
					key_error = False
				else:
					check_opt = False
					key_error = True

				if not key_error:
					encrypted_msg = self.encrypt_blob(unencrypted_file.read_bytes(), public_key.read_bytes())
					enc_cipher = Path(str(encrypted_file))
					enc_cipher.touch(mode=0o600)
					enc_cipher.write_bytes(encrypted_msg)
					print('\nDestination path : %s' % dest_path)
					print('Destination file : %s' % (name_file+'.encrypt.rsa'))
					print('Origin file      : %s' % name_file)

			if cipher_act == 'decrypt':
				check_opt = True
				arg_error = False
				private_key = Path('cipher/.private.pem.rsa.key')
				public_key  = Path('cipher/.public.pem.rsa.key')
				check_file  = open(file_path,'r')
				check_file.close()

				file_ext   = re.split('; |, |\/', file_path)
				name_file  = file_ext[len(file_ext)-1]
				pure_name  = re.split('; |, |\.encrypt.rsa', name_file)
				get_pure   = pure_name[0]
				pure_name2 = re.split('; |, |\.', get_pure)

				encrypted_file = Path(file_path)
				decrypted_file = pure_name[0]+'.decrypt.rsa'

				read_cipher = open(str(encrypted_file), 'rb')
				encrypted_msg = read_cipher.read()
				read_cipher.close()

				final_file = str(decrypted_file)
				decrypted_msg = self.decrypt_blob(encrypted_msg, private_key.read_bytes())

				dec_cipher = open(str(os.getcwd())+'/cipher/'+decrypted_file, 'w+')
				dec_cipher.write(str(decrypted_msg)+'\n')
				dec_cipher.close()
				print('\nDestination path : %s' % dest_path)
				print('Destination file : %s' % final_file)
				print('Origin file      : %s' % name_file)

			if check_opt:
				frmt_query = '{:.3f}'.format(time.time() - go_time)
				print("\nCipher successfully saved as %s" % self.clr(final_file,'g'))
				print("Cipher only can be decrypt using the same "+self.clr('private key','g')+" as it used to encrypt the file")
				print('\n'+self.clr('Query finished successfully in','y')+' %s seconds ...' % (frmt_query))
			else:
				print('')
				if arg_error:
					print("The only valid arguments for the process are "+self.clr("encrypt",'g')+" and "+self.clr("decrypt",'g'))
				if key_error:
					print('Make sure to answer either '+self.clr('y','g')+' or '+self.clr('n','g')+' to handle the public and private key')
				print('Please verify what the action needed to do with the source file')
		except:
			curdate = datetime.datetime.now()
			fldate  = curdate.strftime('%m-%Y')
			print("\nPlease verify the source file name and it's path in the correct format")
			print('Check out '+self.clr('log/bug/'+fldate+'.bug.log','g')+' for more detail about this current event')
			bug_logger.bug_logger_proc('RS')


###
###obj = CipherRSA()
###obj.cipher_gen_rsa_proc()
