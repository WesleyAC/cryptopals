#!/usr/bin/env python3.8

import os, hashlib

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

pubkey = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

msgs = []
with open(os.path.join(os.path.dirname(__file__), "data.txt")) as f:
    working_msg = {}
    for i, line in enumerate(f.readlines()):
        line = line.rstrip('\n').split(": ")[1]
        if i%4 == 0:
            working_msg["msg"] = line
        if i%4 == 1:
            working_msg["s"] = int(line)
        if i%4 == 2:
            working_msg["r"] = int(line)
        if i%4 == 3:
            working_msg["m"] = int(line, 16)
            msgs.append(working_msg)
            working_msg = {}

m1 = None
m2 = None

for m1_m in msgs:
    for m2_m in msgs:
        if m1_m != m2_m and m1_m["r"] == m2_m["r"]:
            m1 = m1_m
            m2 = m2_m

def recover_privkey(data, signature, k):
    r, s = signature
    h = int(hashlib.sha1(data.encode()).hexdigest(), 16)
    return (((s * k) - h) * pow(r, -1, q)) % q

k = (((m1["m"] - m2["m"]) % q) * pow((m1["s"] - m2["s"]), -1, q)) % q
privkey = recover_privkey(m1["msg"], (m1["r"], m1["s"]), k)
print(f"found privkey! {privkey}")
print(f"sha1: {hashlib.sha1(format(privkey, 'x').encode()).hexdigest()}")
