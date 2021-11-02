#!/usr/bin/env python3.8

import hashlib, re
import Crypto.Util.number

def genkey():
    while True:
        try:
            p = Crypto.Util.number.getPrime(1024)
            q = Crypto.Util.number.getPrime(1024)
            n = p * q
            et = (p-1)*(q-1)
            e = 3
            d = pow(e, -1, et)
            break
        except ValueError:
            pass

    return { "e": e, "n": n, "d": d }

def sign(data, key):
    data_hash = hashlib.sha1(data.encode()).hexdigest()
    # PKCS1v.1.5 details copied from https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2, i don't really trust that they're "right" but they will work.
    message_padded = int(f"0001ffffffffffffffffffffffffffffffffffffffffffffffffffff003021300906052b0e03021a05000414{data_hash}", 16)
    return pow(message_padded, key["d"], key["n"])

def verify(data, signature, key):
    message = pow(signature, key["e"], key["n"])
    message_hash = re.compile("1f[ff]*003021300906052b0e03021a05000414([0-9a-f]{40})").match(format(message, 'x')).group(1)
    correct_hash = hashlib.sha1(data.encode()).hexdigest()
    return correct_hash == message_hash

key = genkey()

print("testing valid signature")
data = "test"
signature = sign(data, key)
print("valid" if verify(data, signature, key) else "invalid")

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

print("testing forged signature")
data = "hi mom"
data_hash = hashlib.sha1(data.encode()).hexdigest()
message_padded = int(f"1f003021300906052b0e03021a05000414{data_hash}fffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", 16)
fake_signature = cuberoot(message_padded)
print("valid" if verify(data, fake_signature, key) else "invalid")
