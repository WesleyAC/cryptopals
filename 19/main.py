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

def generate_ciphertexts():
    out = []
    key = b"ABCDEF0123456789"
    for text in open("data.txt").readlines():
        out.append(ctr_encode(key, 0, codecs.decode(text.encode(), "base64")))
    return out

if __name__ == "__main__":
    ciphers = generate_ciphertexts()

    for cipher in ciphers:
        print(xor_repeat(cipher, [217, 72, 14, 175, 38, 144, 25, 34, 194, 86, 226, 159, 218, 53, 25, 130, 191, 37, 30, 89, 177, 34, 148, 129, 192, 18, 41, 46, 40, 201, 160, 93, 50, 104, 190, 24, 114, 170]))
