#!/usr/bin/env python3.8

import random

p = 37
g = 35

a = random.randint(0,p)
A = (g ** a) % p
b = random.randint(0,p)
B = (g ** b) % p

s1 = (B ** a) % p
s2 = (A ** b) % p

assert s1 == s2
