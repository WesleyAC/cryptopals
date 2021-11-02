#!/usr/bin/env python3.8

import Crypto.Util.number
import binascii, random, base64

# this doesn't get the last character of the plaintext, but i'm happy enough ¯\_(ツ)_/¯

def genkey():
    while True:
        try:
            p = Crypto.Util.number.getPrime(512)
            q = Crypto.Util.number.getPrime(512)
            n = p * q
            et = (p-1)*(q-1)
            e = 2**16+1
            d = pow(e, -1, et)
            break
        except ValueError:
            pass

    return { "e": e, "n": n, "d": d }

def encrypt(message, key):
    m = int(binascii.hexlify(message), 16)
    return pow(m, key["e"], key["n"])

def decrypt(ciphertext, key):
    return pow(ciphertext, key["d"], key["n"])

key = genkey()
plaintext = base64.b64decode("VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ==")
ciphertext = encrypt(plaintext, key)

def oracle(ciphertext):
    return pow(ciphertext, key["d"], key["n"]) % 2 == 0

low_bound = 0
high_bound = key["n"]

while True:
    ciphertext = (ciphertext * pow(2, key["e"], key["n"])) % key["n"]
    if oracle(ciphertext):
        high_bound = (low_bound + high_bound) // 2
    else:
        low_bound = (low_bound + high_bound) // 2
    try:
        print(binascii.unhexlify(format(high_bound, 'x')))
    except:
        pass
    if low_bound == high_bound:
        break

