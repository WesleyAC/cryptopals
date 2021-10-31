#!/usr/bin/env python3.8

import random, hashlib, string

from server import Server
from constants import N, g, k

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

username = "me@wesleyac.com"
password = "incorrect"
print(f"trying login with {username}:{password}")

server = Server()

a = random.randint(0,N)
A = pow(g, a, N)

response0 = server.stage0(username, A)

u = int(hashlib.sha256(f"{A}.{response0['B']}".encode()).hexdigest(), 16)
x = int(hashlib.sha256(f"{response0['salt']}.{password}".encode()).hexdigest(), 16)
S = pow((response0['B'] - k * pow(g, x, N)), (a + u * x), N)
K = hashlib.sha256(f"{S}".encode()).hexdigest()
client_hmac = hmac(K.encode(), f"{response0['salt']}".encode())

response1 = server.stage1(client_hmac)

print(response1)

# ---

username = "me@wesleyac.com"
password = "hunter2"
print(f"trying login with {username}:{password}")

server = Server()

a = random.randint(0,N)
A = pow(g, a, N)

response0 = server.stage0(username, A)

u = int(hashlib.sha256(f"{A}.{response0['B']}".encode()).hexdigest(), 16)
x = int(hashlib.sha256(f"{response0['salt']}.{password}".encode()).hexdigest(), 16)
S = pow((response0['B'] - k * pow(g, x, N)), (a + u * x), N)
K = hashlib.sha256(f"{S}".encode()).hexdigest()
client_hmac = hmac(K.encode(), f"{response0['salt']}".encode())

response1 = server.stage1(client_hmac)

print(response1)

# ---

username = "test@example.com"
print(f"trying attack on {username}, A = 0")

server = Server()

response0 = server.stage0(username, 0)
K = hashlib.sha256(f"0".encode()).hexdigest()
client_hmac = hmac(K.encode(), f"{response0['salt']}".encode())

response1 = server.stage1(client_hmac)

print(response1)

# ---

username = "test@example.com"
print(f"trying attack on {username}, A = N")

server = Server()

response0 = server.stage0(username, N)
K = hashlib.sha256(f"0".encode()).hexdigest()
client_hmac = hmac(K.encode(), f"{response0['salt']}".encode())

response1 = server.stage1(client_hmac)

print(response1)

# ---

username = "test@example.com"
print(f"trying attack on {username}, A = 2N")

server = Server()

response0 = server.stage0(username, N*2)
K = hashlib.sha256(f"0".encode()).hexdigest()
client_hmac = hmac(K.encode(), f"{response0['salt']}".encode())

response1 = server.stage1(client_hmac)

print(response1)
