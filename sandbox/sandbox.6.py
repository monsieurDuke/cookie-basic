import hashlib
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

read_plain = open(r'/home/cookie/Sandbox/Cookie-Basic/cipher/sample-plain.txt', 'r')
plain_str  = read_plain.read()
read_plain.close()

read_rot13key = open(r'/home/cookie/Sandbox/Cookie-Basic/cipher/cipher-rot13.key', 'r')
rot13_str = read_rot13key.read()
read_rot13key.close()

def str_to_char(text):
    return [char for char in text]

plain_char    = str_to_char(plain_str)
cipher_char   = [None]*len(plain_char)
uncipher_char = [None]*len(cipher_char)
cipher_str    = ''
unchiper_str  = ''

rot13_enc  = (str_to_char(rot13_str))*2
count_len  = len(rot13_enc)
rot13_dec  = [None]*count_len
passer     = count_len

## creating the decryption
for i in range(len(rot13_enc)):
    rot13_dec[i] = rot13_enc[passer-1]
    if passer > 0:
        passer -= 1

## encrypting the plain text
for i in range(len(plain_char)):
    for j in range(len(rot13_enc)):
        if plain_char[i] == rot13_enc[j]:
            cipher_char[i] = rot13_enc[j+13]
            cipher_str += cipher_char[i]  
            break

## decrypting the plain text
for i in range(len(cipher_char)):
    for j in range(len(rot13_enc)):
        if cipher_char[i] == rot13_dec[j]:
            uncipher_char[i] = rot13_dec[j+13]
            unchiper_str += uncipher_char[i]
            break

write_cipher = open('/home/cookie/Sandbox/Cookie-Basic/cipher/sample-plain.txt.crpyt','w')
write_cipher.write(cipher_str+'\n')
write_cipher.close()

print('PLAIN TEXT:\n'+plain_str+'\n')
print('ROT13 ENCRYOTED:\n'+cipher_str+'\n')
print('ROT13 DECRYPTED:\n'+unchiper_str+'\n')
