#!/usr/bin/env python3.8

import os
from Crypto.Cipher import AES

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

random_key = os.urandom(16)

def encrypt(data):
    cipher = AES.new(random_key, AES.MODE_CBC, random_key)
    return cipher.encrypt(pkcs7_pad(data, len(random_key)))

def decrypt(data):
    cipher = AES.new(random_key, AES.MODE_CBC, random_key)
    out = cipher.decrypt(data)
    if not all(c < 128 for c in out):
        return out # error
    else:
        return None # good

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

if __name__ == "__main__":
    out = encrypt(b"________________")
    plain = b"This is a string that is designed to be at least three blocks long, but is probably many more :)"
    msg = encrypt(plain)
    print(f"key (SECRET!): {random_key}")
    edited_msg = msg[:16] + bytes([0]*16) + msg[:16]
    err = decrypt(edited_msg)
    print(err)
    found_key = xor_repeat(err[:16], err[32:48])
    print(f"found key: {found_key}")
