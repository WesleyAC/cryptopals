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

mt = [0]*n
index = n + 1

lower_mask = (1 << r) - 1
upper_mask = (1 << w) - 1 - lower_mask
 
# Initialize the generator from a seed
def seed_mt(seed):
    global index
    index = n
    mt[0] = seed

    for i in range(1, n):
        mt[i] = (f * (mt[i-1] ^ (mt[i-1] >> (w-2))) + i) & ((1 << w) - 1)
 
# Extract a tempered value based on MT[index]
# calling twist() every n numbers
def extract_number():
    global index
    if index >= n:
        if index > n:
            print("error: generator was not seeded")
        twist()
 
    y = mt[index]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
 
    index += 1
    return y & ((1 << w) - 1)
 
# Generate the next n values from the series x_i 
def twist():
    global index
    for i in range(0, n):
        x = (mt[i] & upper_mask) + (mt[(i+1) % n] & lower_mask)
        xA = x >> 1
        if (x % 2) != 0:
            xA = xA ^ a
        mt[i] = mt[(i + m) % n] ^ xA
    index = 0

if __name__ == "__main__":
    seed_mt(1)
    out = extract_number()
    print(out)
    assert out == 1791095845 # result from c++ std::mt19937
