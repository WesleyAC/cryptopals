#!/usr/bin/env python3

import codecs, math
from collections import Counter

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
        counts = Counter(text)
        return sum([counts[x] for x in ['a', 'e', 'i', 'o', 'u', ' ']]) / len(text)
    except UnicodeError:
        return 0

def crack_single_byte_xor(cyphertext):
    outs = [(single_byte_xor(cyphertext, k), k) for k in range(256)]
    outs = [(english_score(text[0]), text) for text in outs]
    return sorted(outs)[-1][1][1]

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

if __name__ == "__main__":
    cyphertext = codecs.decode(open("data.txt").read().encode(), "base64")

    keysizes = {}
    for keysize in range(2, 40):
        dist_sum = 0
        num_blocks = math.floor(len(cyphertext) / keysize) - 1
        for i in range(num_blocks):
            dist_sum += hamming_dist(cyphertext[keysize*i:keysize*i+keysize], cyphertext[keysize*i+keysize:keysize*i+keysize*2]) / keysize
        keysizes[keysize] = dist_sum / num_blocks

    keysize = min(keysizes, key=keysizes.get)

    transposed_blocks = []
    for i in range(keysize):
        transposed_blocks.append(cyphertext[i::keysize])

    key = bytearray()
    for block in transposed_blocks:
        key.append(crack_single_byte_xor(block))

    print(codecs.decode(xor_repeat(cyphertext, key)))
