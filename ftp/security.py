# -*- coding: UTF-8 -*-

import base, base64
from Crypto.Cipher import AES
import os


# extracting the string from the datafile.
def from_file(file_name, file_path=None):
    if file_path:
        file_name = file_path + os.sep + file_name
    raw_str = ''
    try:
        f = open(file_name, 'r')
        lines = f.readlines()
        for line in lines:
            raw_str = raw_str + line
        f.close()
    except Exception as e:
        print(e)
    return raw_str


# store the string which were encoding
def to_file(raw_str, file_name, file_path=None):
    if file_path:
        file_name = file_path + os.sep + file_name
    try:
        tar = open(file_name, 'wb')
        tar.write(raw_str)
        tar.close()
        print('successfully store to the file %s' %(file_name))
        return True
    except Exception as e:
        print(e)
        return False


def encry_file(file_name, file_path=None, key=base.CRYPT_KEY):
    raw_str = from_file(file_name, file_path)
    rest = 0
    if len(raw_str) % base.CRYPT_LENGTH != 0:
        rest = base.CRYPT_LENGTH - len(raw_str) % base.CRYPT_LENGTH
    raw_str = raw_str + ('\000' * rest)
    encry_obj = AES.new(key, AES.MODE_ECB)
    encry_str = encry_obj.encrypt(raw_str)
    encry_str = base64.b64encode(encry_str)
    print('successfully encoding')
    return to_file(encry_str, file_name)


def decrypt_file(file_name, file_path=None, key=base.CRYPT_KEY):
    raw_str = from_file(file_name, file_path)
    # lens = len(raw_str)
    lenx = 4 - len(raw_str) % 4
    try:
        raw_str = raw_str + b'=' * lenx
    except:
        pass
    raw_str = base64.b64decode(raw_str)
    rest = 0
    if len(raw_str) % base.CRYPT_LENGTH != 0:
        rest = base.CRYPT_LENGTH - len(raw_str) % base.CRYPT_LENGTH
    raw_str = raw_str + ('\000' * rest)
    encry_obj = AES.new(key, AES.MODE_ECB)
    decrypt_str = encry_obj.decrypt(raw_str)
    print('successfully decoding')
    return to_file(decrypt_str, file_name)
