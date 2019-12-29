#!/usr/bin/env python3

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

import time

def reset_token():
    rand = MT19937()
    seed = int(round(time.time() * 1000))
    rand.seed_mt(seed)
    return rand.extract_number()

def verify_token(token):
    seed = int(round(time.time() * 1000))
    for i in range(seed - 100, seed + 100):
        rand = MT19937()
        rand.seed_mt(i)
        if rand.extract_number() == token:
            return True
    return False



if __name__ == "__main__":
    token = reset_token()
    print(token)
    assert verify_token(token)
    assert not verify_token(1234)
    assert not verify_token(42)
    assert not verify_token(432432)
