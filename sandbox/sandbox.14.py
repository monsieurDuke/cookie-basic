from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

keypair = RSA.generate(2048)

pubkey    = keypair.publickey()
pubkeyPEM = pubkey.exportKey()
prvkeyPEM = keypair.exportKey()

n_public  = {hex(pubkey.n)}
n_keypair = {hex(keypair.d)}

#print(pubkeyPEM.decode('ascii'))
#print('Private Key : %s' % n_keypair)
#print(prvkeyPEM.decode('ascii'))

#logs = open('buglogger.log', 'a')
#logs.write('[%s %s] (NS) ERROR: %s\n' % (getdate, gettime,error_info))
#logs.close()

anw = input('action needed : ')
if anw == 'encrypt':
	msg_str    = (input('plain text: '))
	message    = msg_str.encode("utf-8")
	encryptor  = PKCS1_OAEP.new(pubkey)
	cipher_enc = encryptor.encrypt(message)

	print('Encrypted   : %s' % (binascii.hexlify(cipher_enc)))
	save_cipher = open('cipher.csv', 'wb')
	save_cipher.write(binascii.hexlify(cipher_enc))
	save_cipher.close()

	print(prvkeyPEM.decode('ascii'))
	save_privkey = open('privatekey.pem', 'wb')
	save_privkey.write(keypair.exportKey())
	save_privkey.close()

	print(len(binascii.hexlify(cipher_enc)))

	decryptor  = PKCS1_OAEP.new(keypair)
	cipher_dec = decryptor.decrypt(cipher_enc)
	print('Decrypted: %s' % (cipher_dec))

else:
	read_cipher = open('cipher.csv','rb')
	cipher_enc  = read_cipher.read()
	read_cipher.close()

	read_privkey = open('privatekey.pem', 'rb')
	key_dec = RSA.importKey(read_privkey.read())
	read_privkey.close()

	print(len(cipher_enc))

	decryptor  = PKCS1_OAEP.new(key_dec)
	cipher_dec = decryptor.decrypt(cipher_enc)
	print('Decrypted: %s' % (cipher_dec))
