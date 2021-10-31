#!/usr/bin/env python3.8

from Crypto.Cipher import AES
import hashlib, os, random

a_p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
a_g = 2

a_a = random.randint(0,a_p)
a_A = pow(a_g, a_a, a_p)

# A -> M (a_p, a_g, a_A)

m_p = a_p
m_g = a_g
m_A = a_A

b_p = m_p
b_g = 1 # attack!
b_A = m_A

# M -> B (a_p, a_g, a_p)

b_b = random.randint(0,b_p)
b_B = pow(b_g, b_b, b_p)
b_s = pow(b_A, b_b, b_p)

# B -> M (b_B)

m_B = b_B

a_B = m_B

# M -> A (m_p)

a_s = pow(a_B, a_a, a_p)

a_key = hashlib.sha1(a_s.to_bytes(256, 'little')).digest()[:16]
a_iv = os.urandom(16)
a_cipher = AES.new(a_key, AES.MODE_CBC, a_iv)
a_ct = a_cipher.encrypt(b"YELLOW SUBMARINE")

# A -> M (a_ct, a_iv)

m_a_ct = a_ct
m_a_iv = a_iv

m_s = 1
m_key = hashlib.sha1(m_s.to_bytes(256, 'little')).digest()[:16]
m_a_decrypt_cipher = AES.new(m_key, AES.MODE_CBC, m_a_iv)
m_a_pt = m_a_decrypt_cipher.decrypt(m_a_ct)

print(f"M has received message: {m_a_pt}")
