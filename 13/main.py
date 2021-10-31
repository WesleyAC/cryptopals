#!/usr/bin/env python3.8

import os
from Crypto.Cipher import AES

def parse_kv(s):
    obj = {}
    for part in s.split(b"&"):
        k, v = part.split(b"=")
        obj[k] = v
    return obj

def profile_for(user):
    user = user.replace(b"&", b"_").replace(b"=", b"_")
    return f"email={user.decode()}&uid=10&role=user".encode()

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

oracle_key = os.urandom(16)

def encrypt(username):
    plaintext = profile_for(username)
    cipher = AES.new(oracle_key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(plaintext, len(oracle_key)))

def decrypt(cyphertext):
    cipher = AES.new(oracle_key, AES.MODE_ECB)
    result = cipher.decrypt(cyphertext)
    return result[:-result[-1]]

# email=me______________@wesleyac.com&uid=10&role=user
# 0123456789abcdef                0123456789abcdef
#                 0123456789abcdef                0123456789abcdef

# email=me________adminPADDINGBYTE&uid=10&role=user
# 0123456789abcdef                0123456789abcdef
#                 0123456789abcdef                0123456789abcdef

if __name__ == "__main__":
    admin_chunk = list(chunks(encrypt(b"__________admin" + bytes([11]*11)), 16))[1]
    beginning = list(chunks(encrypt(b"me______________@wesleyac.com"), 16))
    admin_cookie = b"".join(beginning[:3] + [admin_chunk])
    print(decrypt(admin_cookie))
