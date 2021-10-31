#!/usr/bin/env python3
import random, hashlib

from constants import N, g, k
from server import Server
from mitm import Mitm
from util import hmac

# server = Server()
server = Mitm()

a = random.randint(0,N)
A = pow(g, a, N)

response0 = server.stage0("me@wesleyac.com", A)
salt = response0["salt"]
B = response0["B"]
u = response0["u"]

password = "madeline"

x = int(hashlib.sha256(f"{salt}.{password}".encode()).hexdigest(), 16)
S = pow(B, (a + u*x), N)
K = hashlib.sha256(f"{S}".encode()).hexdigest()

client_hmac = hmac(K.encode(), f"{salt}".encode())

print(server.stage1(client_hmac))

server.crack_password()
