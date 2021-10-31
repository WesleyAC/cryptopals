#!/usr/bin/env python3.8

import os, math
from Crypto.Cipher import AES

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

def ctr_encode(key, nonce, data):
    cipher = AES.new(key, AES.MODE_ECB)
    out = bytearray([])
    for i in range(math.ceil(len(data) / 16)):
        x = cipher.encrypt(nonce.to_bytes(8, byteorder='little') + i.to_bytes(8, byteorder='little'))
        out += xor_repeat(data[i*16:(i+1)*16], x)
    return out

random_key = os.urandom(16)
iv = os.urandom(16)

def encrypt(userdata):
    userdata = userdata.replace(b";", b"").replace(b"=", b"")
    data = b"comment1=cooking%20MCs;userdata=" + userdata + b";comment2=%20like%20a%20pound%20of%20bacon"
    return ctr_encode(random_key, 0, data)

def is_admin(data):
    return b";admin=true;" in ctr_encode(random_key, 0, data)

# comment1=cooking%20MCs;userdata=00000000000000000000000000000000;comment2=%20like%20a%20pound%20of%20bacon
# 0123456789abcdef                0123456789abcdef                0123456789abcdef                0123456789abcdef
#                 0123456789abcdef                0123456789abcdef                0123456789abcdef
# now we know the keystream for   ________________________________ these blocks, so we can generate arbitrary text
# replace these with              me_____@wesleyac.com;admin=true;

if __name__ == "__main__":
    out = encrypt(bytes([0]*32))
    new = xor_repeat(b"me_____@wesleyac.com;admin=true;", out[32:64])
    final = out[:32] + new + out[64:]
    print(final)
    admin = is_admin(final)
    print(admin)
    assert admin
