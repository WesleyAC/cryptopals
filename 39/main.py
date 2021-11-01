#!/usr/bin/env python3.8

import Crypto.Util.number
import binascii, math

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
        pass # invmod failed (since i'm not picking safe primes), try some new primes until e is coprime with et i guess?

plaintext = "sphinx of black quartz, judge my vow. "*2
m = int(binascii.hexlify(plaintext.encode()), 16)

c = pow(m, e, n)
decrypted = pow(c, d, n)

print(binascii.unhexlify(format(decrypted, 'x')))
