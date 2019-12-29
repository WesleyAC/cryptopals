#!/usr/bin/env python3

import codecs, math, os
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

secret_key = os.urandom(16)

def edit_ciphertext(ct, offset, newtext):
    plaintext = ctr_encode(secret_key, 0, ct)
    plaintext = plaintext[:offset] + newtext + plaintext[offset+len(newtext):]
    return ctr_encode(secret_key, 0, plaintext)

if __name__ == "__main__":
    ct = ctr_encode(secret_key, 0, open("plain.txt").read().encode())
    orig_ct = ct
    for i in range(len(ct) // 16):
        ct = edit_ciphertext(ct, i*16, bytes([0]*16))
        print(xor_repeat(orig_ct[i*16:(i+1)*16], ct[i*16:(i+1)*16]))
