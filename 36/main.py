#!/usr/bin/env python3

import random, hashlib

def xor_bytes(i1, i2):
    return bytes(a ^ b for a, b in zip(i1, i2))

def hmac(key, msg):
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    if len(key) < 64:
        key = key + bytes([0] * (64 - len(key)))

    o_key_pad = xor_bytes(key, [0x5c] * 64)
    i_key_pad = xor_bytes(key, [0x36] * 64)

    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + msg).digest()).digest()

# C & S
# i'm assuming "agree on" means hardcode?
N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3
I = "me@wesleyac.com" # not actually really used in this example but whatevs
P = "hunter2"

# S
salt = random.randint(0,2**128)
S_xH = hashlib.sha256(f"{salt}.{P}".encode()).hexdigest()
S_x = int(S_xH, 16)
v = pow(g, S_x, N)
del S_x
del S_xH

# C -> S (I, A)
a = random.randint(0,N)
A = pow(g, a, N)

# S -> C (salt, B)
b = random.randint(0,N)
B = k*v + pow(g, b, N)

# S, C
uH = hashlib.sha256(f"{A}.{B}".encode()).hexdigest()
u = int(uH, 16)

# C
C_xH = hashlib.sha256(f"{salt}.{P}".encode()).hexdigest()
C_x = int(C_xH, 16)
# does the mod N in the inner pow call cause problems?
C_S = pow((B - k * pow(g, C_x, N)), (a + u * C_x), N)
C_K = hashlib.sha256(f"{C_S}".encode()).hexdigest()

# S
# does the mod N in the inner pow call cause problems?
S_S = pow((A * pow(v, u, N)), b, N)
S_K = hashlib.sha256(f"{S_S}".encode()).hexdigest()

# C -> S
C_hmac = hmac(C_K.encode(), f"{salt}".encode())

# S -> C

S_hmac = hmac(S_K.encode(), f"{salt}".encode())

if S_hmac == C_hmac:
    print("OK")
else:
    print("ERR")
