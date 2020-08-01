import hashlib
import binascii
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def cipher_gen_rot13_proc():
    file_path  = input('FUll Path of Source : ')
    cipher_act = input('Action of Cipher    : ')

    file_ext   = re.split('; |, |\/', file_path)
    name_file  = file_ext[len(file_ext)-1]
    read_plain = open(file_path, 'r')
    plain_str  = read_plain.read()
    read_plain.close()

    read_rot13key = open('/home/cookie/Sandbox/Cookie-Basic/cipher/cipher-rot13.key', 'r')
    rot13_str = read_rot13key.read()
    read_rot13key.close()

    plain_char    = str_to_char(plain_str)
    cipher_char   = [None]*len(plain_char)
    uncipher_char = [None]*len(cipher_char)
    cipher_str    = ''
    uncipher_str  = ''
    get_final     = ''

    rot13_enc  = (str_to_char(rot13_str))*2
    count_len  = len(rot13_enc)
    rot13_dec  = [None]*count_len
    passer     = count_len

    for i in range(len(rot13_enc)):
        rot13_dec[i] = rot13_enc[passer-1]
        if passer > 0:
            passer -= 1

    if cipher_act == 'encrypt':
        get_final = rot13_encypt(plain_char, rot13_enc, cipher_char, cipher_str, file_path)
    if cipher_act == 'decrypt':
        get_final = rot13_decrypt(plain_char, rot13_enc, rot13_dec, uncipher_char, uncipher_str, file_path)

    get_result = re.split('; |, |\#', get_final)
    print('Cipher successfully saved as %s' % get_result[len(get_result)-1])

def str_to_char(text):
    return [char for char in text]

## encrypting the plain text
def rot13_encypt(plain_char, rot13_enc, cipher_char, cipher_str, file_path):
    print('path: %s' % file_path)
    for i in range(len(plain_char)):
        for j in range(len(rot13_enc)):
            if plain_char[i] == rot13_enc[j]:
                cipher_char[i] = rot13_enc[j+13]
                cipher_str += cipher_char[i]
                break

    file_ext   = re.split('; |, |\/', file_path)
    name_file  = file_ext[len(file_ext)-1]
    pure_file  = ''
    file_path  = ''

    try:
        get_pure = re.split('; |, |\.encrypt.', name_file)
        pure_file = get_pure[0]+'.encrypt.r13'
    except:
        try:
            get_pure = re.split('; |, |\.decrypt.', name_file)
            pure_file = get_pure[0]+'.encrypt.r13'
        except:
            pure_file = name_file+'.encrypt.r13'

    file_path = '/home/cookie/Sandbox/Cookie-Basic/cipher/'+pure_file

    print('pure: '+pure_file)
    print('name: '+name_file)
    write_cipher = open(file_path,'w')
    write_cipher.write(cipher_str)
    write_cipher.close()
    return cipher_str+'#'+pure_file

## decrypting the plain text
def rot13_decrypt(cipher_char, rot13_enc, rot13_dec, uncipher_char, uncipher_str, file_path):
    print('path: %s' % file_path)
    for i in range(len(cipher_char)):
        for j in range(len(rot13_enc)):
            if cipher_char[i] == rot13_dec[j]:
                uncipher_char[i] = rot13_dec[j+13]
                uncipher_str += uncipher_char[i]
                break

    file_ext   = re.split('; |, |\/', file_path)
    name_file  = file_ext[len(file_ext)-1]
    pure_file  = ''
    file_path  = ''

    try:
        get_pure = re.split('; |, |\.decrypt.', name_file)
        pure_file = get_pure[0]+'.decrypt.r13'
    except:
        try:
            get_pure = re.split('; |, |\.encrypt.', name_file)
            pure_file = get_pure[0]+'.decrypt.r13'
        except:
            pure_file = name_file+'.decrypt.r13'

    file_path = '/home/cookie/Sandbox/Cookie-Basic/cipher/'+pure_file

    print('pure: '+pure_file)
    print('name: '+name_file)
    write_cipher = open(file_path,'w')
    write_cipher.write(uncipher_str)
    write_cipher.close()
    return uncipher_str+'#'+pure_file

#print('PLAIN TEXT:\n'+plain_str+'\n')
#print('ROT13 ENCRYOTED:\n'+cipher_str+'\n')
#print('ROT13 DECRYPTED:\n'+uncipher_str+'\n')

cipher_gen_rot13_proc()
