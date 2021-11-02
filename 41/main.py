#!/usr/bin/env python3.8

import Crypto.Util.number
import binascii, random

def genkey():
    while True:
        try:
            p = Crypto.Util.number.getPrime(512)
            q = Crypto.Util.number.getPrime(512)
            n = p * q
            et = (p-1)*(q-1)
            e = 3
            d = pow(e, -1, et)
            break
        except ValueError:
            pass

    return { "e": e, "n": n, "d": d }

def encrypt(message, e, n):
    m = int(binascii.hexlify(message.encode()), 16)
    return pow(m, e, n)

def decrypt(ciphertext, d, n):
    return binascii.unhexlify(format(pow(ciphertext, d, n), 'x'))

plaintext= """{
  time: 1356304276,
  social: '555-55-5555',
}"""
key = genkey()
ciphertext = encrypt(plaintext, key["e"], key["n"])

# the goal: make a new ciphertext that, when decrpyted, will allow us to recover the original plaintext.

s = random.randint(1, key["n"]-1)
new_ciphertext = (pow(s, key["e"], key["n"]) * ciphertext) % key["n"]

# server does the next two lines
assert ciphertext != new_ciphertext
response = decrypt(new_ciphertext, key["d"], key["n"])

response_int = int(binascii.hexlify(response), 16)
recovered_plaintext = response_int * pow(s, -1, key["n"]) % key["n"]
print(binascii.unhexlify(format(recovered_plaintext, 'x')))
