#!/usr/bin/env python3.8

w = 32
n = 624
m = 397
r = 31

a = 0x9908B0DF

u = 11
d = 0xFFFFFFFF
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18

f = 1812433253

lower_mask = (1 << r) - 1
upper_mask = (1 << w) - 1 - lower_mask

class MT19937:
    def __init__(self):
        self.mt = [0]*n
        self.index = n + 1
     
    # Initialize the generator from a seed
    def seed_mt(self, seed):
        self.index = n
        self.mt[0] = seed

        for i in range(1, n):
            self.mt[i] = (f * (self.mt[i-1] ^ (self.mt[i-1] >> (w-2))) + i) & ((1 << w) - 1)
     
    # Extract a tempered value based on mt[index]
    # calling twist() every n numbers
    def extract_number(self):
        if self.index >= n:
            if self.index > n:
                print("error: generator was not seeded")
            self.twist()
     
        y = self.mt[self.index]
        y = y ^ ((y >> u) & d)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)
        y = y ^ (y >> l)
     
        self.index += 1
        return y & ((1 << w) - 1)
     
    # Generate the next n values from the series x_i 
    def twist(self):
        for i in range(0, n):
            x = (self.mt[i] & upper_mask) + (self.mt[(i+1) % n] & lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ a
            self.mt[i] = self.mt[(i + m) % n] ^ xA
        self.index = 0

import math, os, random

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

def transform_stream(seed, text):
    rand = MT19937()
    rand.seed_mt(seed)
    out = bytearray()
    for i in range(math.ceil(len(text) / 4)):
        keystream = rand.extract_number().to_bytes(4, 'little')
        out += xor_repeat(text[i*4:(i+1)*4], keystream)
    return out

if __name__ == "__main__":
    secret_key = int.from_bytes(os.urandom(2), 'little')
    print(f"key (SECRET! DON'T LOOK!): {secret_key}")
    ct = transform_stream(secret_key, os.urandom(random.randint(40, 300)) + bytes([42]*14))
    for i in range(2**16):
        rand = MT19937()
        rand.seed_mt(i)
        for _ in range(math.floor((len(ct) - 14) / 4)): rand.extract_number()
        cut = (len(ct) - 14) % 4
        keystream = bytearray()
        for _ in range(5):
            keystream += rand.extract_number().to_bytes(4, 'little')
        keystream = keystream[cut:cut+14]
        encrypted_stream = bytes(map(lambda x: x ^ 42, keystream))
        if encrypted_stream == ct[-14:]:
            print(f"found key! {i}")
            break
