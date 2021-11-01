#!/usr/bin/env python3.8

import Crypto.Util.number
import binascii

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

    return {
        "n": n,
        "e": e,
    }

def encrypt(message, e, n):
    m = int(binascii.hexlify(message.encode()), 16)
    return pow(m, e, n)

plaintext = "sphinx of black quartz, judge my vow."

key0 = genkey()
key1 = genkey()
key2 = genkey()

c0 = encrypt(plaintext, key0["e"], key0["n"])
c1 = encrypt(plaintext, key1["e"], key1["n"])
c2 = encrypt(plaintext, key2["e"], key2["n"])

def cuberoot(x):
    high = 1
    while high ** 3 < x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**3 < x:
            low = mid
        elif high > mid and mid**3 > x:
            high = mid
        else:
            return mid
    return mid + 1

ms0 = key1["n"] * key2["n"]
ms1 = key0["n"] * key2["n"]
ms2 = key0["n"] * key1["n"]
result = cuberoot((
  (c0 * ms0 * pow(ms0, -1, key0["n"])) +
  (c1 * ms1 * pow(ms1, -1, key1["n"])) +
  (c2 * ms2 * pow(ms2, -1, key2["n"]))) %
  (key0["n"] * key1["n"] * key2["n"])
)

print(binascii.unhexlify(format(result, 'x')))
