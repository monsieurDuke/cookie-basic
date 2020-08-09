from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

key = RSA.generate(4096)
f = open('my_rsa_public.pem', 'wb')
f.write(key.publickey().exportKey('PEM'))
f.close()

f = open('my_rsa_private.pem', 'wb')
f.write(key.exportKey('PEM'))
f.close()

f1 = open('my_rsa_public.pem', 'rb')
f2 = open('my_rsa_private.pem', 'rb')
key1  = RSA.importKey(f1.read())
key2 = RSA.importKey(f2.read())

x = key1.encrypt(b"yeeeeeeeeeet",32)

print(x)
z = key2.decrypt(x)
print(z)
