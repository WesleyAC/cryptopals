#!/usr/bin/env python3

import codecs, math, os
from Crypto.Cipher import AES
from collections import Counter

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

def ctr_encode(key, nonce, data):
    cipher = AES.new(key, AES.MODE_ECB)
    out = bytearray([])
    for i in range(math.ceil(len(data) / 16)):
        x = cipher.encrypt(nonce.to_bytes(8, byteorder='little') + i.to_bytes(8, byteorder='little'))
        out += xor_repeat(data[i*16:(i+1)*16], x)
    return out

def generate_ciphertexts():
    out = []
    key = os.urandom(16)
    for text in open("data.txt").readlines():
        out.append(ctr_encode(key, 0, codecs.decode(text.encode(), "base64")))
    return out

def hamming_dist(a, b):
    assert len(a) == len(b)
    dist = 0
    for i in range(len(a)):
        dist += bin(a[i] ^ b[i]).count("1")
    return dist

def single_byte_xor(cyphertext, key):
    return bytes([e ^ key for e in cyphertext])

def english_score(text):
    try:
        text = text.decode()
        counts = Counter(text.lower())
        return sum([counts[x] for x in ['e', 't', 'a', 'o', 'i', ' ']]) / len(text)
    except UnicodeError:
        return 0

def crack_single_byte_xor(cyphertext):
    outs = [(single_byte_xor(cyphertext, k), k) for k in range(256)]
    outs = [(english_score(text[0]), text) for text in outs]
    return sorted(outs)[-1][1][1]

if __name__ == "__main__":
    ciphers = generate_ciphertexts()
    keysize = min(map(lambda x: len(x), ciphers))
    truncated_ciphers = list(map(lambda x: x[:keysize], ciphers))
    ciphertext = b"".join(truncated_ciphers)

    transposed_blocks = []
    for i in range(keysize):
        transposed_blocks.append(ciphertext[i::keysize])

    key = bytearray()
    for block in transposed_blocks:
        key.append(crack_single_byte_xor(block))

    for cipher in ciphers:
        print(xor_repeat(cipher[:keysize], key))
