#!/usr/bin/env python3

import codecs, math
from Crypto.Cipher import AES

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

def ctr_decrypt(key, nonce, data):
    cipher = AES.new(key, AES.MODE_ECB)
    out = bytearray([])
    for i in range(math.ceil(len(data) / 16)):
        x = cipher.encrypt(nonce.to_bytes(8, byteorder='little') + i.to_bytes(8, byteorder='little'))
        out += xor_repeat(data[i*16:(i+1)*16], x)
    return out

if __name__ == "__main__":
    print(ctr_decrypt(b"YELLOW SUBMARINE", 0, codecs.decode(b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==", "base64")))
