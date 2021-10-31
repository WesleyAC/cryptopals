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

def untemper(y):
    def unshr(x, shr):
        r = x
        for i in range(32):
            r = x ^ (r >> shr)
        return r

    def unshl(x, shl, mask):
        r = x
        for i in range(32):
            r = x ^ (r << shl & mask)
        return r

    y = unshr(y, l)
    y = unshl(y, t, c)
    y = unshl(y, s, b)
    y = unshr(y, u) # mask not needed, since d is all 1s anyways
    return y & ((1 << w) - 1)

import os

if __name__ == "__main__":
    g = MT19937()
    g.seed_mt(int.from_bytes(os.urandom(4), "little"))
    out = []
    for i in range(624):
        out.append(g.extract_number())
    state = []
    for z in out:
        state.append(untemper(z))
    cloned = MT19937()
    cloned.mt = state
    cloned.index = 624
    for i in range(100):
        cloned_num = cloned.extract_number()
        print(cloned_num)
        assert g.extract_number() == cloned_num
