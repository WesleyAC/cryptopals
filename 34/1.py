#!/usr/bin/env python3.8

from Crypto.Cipher import AES
import hashlib, os, random

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

a = random.randint(0,p)
A = pow(g, a, p)

# A -> B (p, g, A)

b = random.randint(0,p)
B = pow(g, b, p)
b_s = pow(B, a, p)

# B -> A (B)

a_s = pow(A, b, p)

a_key = hashlib.sha1(a_s.to_bytes(256, 'little')).digest()[:16]
a_iv = os.urandom(16)
a_cipher = AES.new(a_key, AES.MODE_CBC, a_iv)
a_ct = a_cipher.encrypt(b"YELLOW SUBMARINE")

# A -> B (a_ct, a_iv)

b_key = hashlib.sha1(b_s.to_bytes(256, 'little')).digest()[:16]
b_decrypt_cipher = AES.new(b_key, AES.MODE_CBC, a_iv)
b_pt = b_decrypt_cipher.decrypt(a_ct)

print(f"B has received message: {b_pt}")

b_iv = os.urandom(16)
b_encrypt_cipher = AES.new(b_key, AES.MODE_CBC, b_iv)
b_ct = b_encrypt_cipher.encrypt(b_pt)

# B -> A (b_ct, b_iv)

a_decrypt_cipher = AES.new(a_key, AES.MODE_CBC, b_iv)
a_pt = a_decrypt_cipher.decrypt(b_ct)

print(f"A has received message: {a_pt}")
