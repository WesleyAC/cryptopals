#!/usr/bin/env python3.8

import os
from Crypto.Cipher import AES

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

random_key = os.urandom(16)
iv = os.urandom(16)

def encrypt(userdata):
    userdata = userdata.replace(b";", b"").replace(b"=", b"")
    data = b"comment1=cooking%20MCs;userdata=" + userdata + b";comment2=%20like%20a%20pound%20of%20bacon"
    cipher = AES.new(random_key, AES.MODE_CBC, iv)
    return cipher.encrypt(pkcs7_pad(data, len(random_key)))

def is_admin(data):
    cipher = AES.new(random_key, AES.MODE_CBC, iv)
    return b";admin=true;" in cipher.decrypt(data)

# comment1=cooking%20MCs;userdata=________________;comment2=%20like%20a%20pound%20of%20bacon
# 0123456789abcdef                0123456789abcdef                0123456789abcdef
#                 0123456789abcdef                0123456789abcdef                0123456789abcdef

if __name__ == "__main__":
    out = encrypt(b"________________")
    new_block = bytearray(out[32:48])
    replace =      b";comment2=%20lik"
    replace_with = b";admin=true;____"
    for i in range(16):
        new_block[i] = new_block[i] ^ replace_with[i] ^ replace[i]
    final = out[:32] + new_block + out[48:]
    print(is_admin(final))
