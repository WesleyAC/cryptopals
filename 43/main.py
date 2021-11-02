#!/usr/bin/env python3.8

# yeah, yeah, random isn't a CSPRNG, do i look like i give a fuck?
import random, hashlib

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

def keygen():
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    return { "privkey": x, "pubkey": y }

def sign(data, privkey, k = None):
    # TODO: check for r=0 or s=0
    if k is None:
        k = random.randint(1, q-1)
    r = pow(g, k, p) % q
    h = int(hashlib.sha1(data.encode()).hexdigest(), 16)
    s = (pow(k, -1, q) * (h + privkey * r)) % q
    return (r, s)

def verify(data, signature, pubkey):
    r, s = signature
    assert 0 < r < q and 0 < s < q
    w = pow(s, -1, q)
    h = int(hashlib.sha1(data.encode()).hexdigest(), 16)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(pubkey, u2, p) % p) % q
    return v == r

key = keygen()
message = "test"
known_k_value = 1234567890
signature = sign(message, key["privkey"], known_k_value)
assert verify(message, signature, key["pubkey"])

def recover_privkey(data, signature, k):
    r, s = signature
    h = int(hashlib.sha1(data.encode()).hexdigest(), 16)
    return (((s * k) - h) * pow(r, -1, q)) % q

assert recover_privkey(message, signature, known_k_value) == key["privkey"]

y = 0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17
data = "For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n"
assert hashlib.sha1(data.encode()).hexdigest() == "d2d0714f014a9784047eaeccf956520045c45265"
signature = (548099063082341131477253921760299949438196259240, 857042759984254168557880549501802188789837994940)

for possible_k in range(1, 2**16):
    possible_privkey = recover_privkey(data, signature, possible_k)
    if sign(data, possible_privkey, possible_k) == signature:
        print(f"found privkey! {possible_privkey}")
        print(f"sha1: {hashlib.sha1(format(possible_privkey, 'x').encode()).hexdigest()}")
        exit()
