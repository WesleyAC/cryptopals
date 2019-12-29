#!/usr/bin/env python3

import codecs
from collections import Counter

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
    outs = [single_byte_xor(cyphertext, k) for k in range(256)]
    outs = [(english_score(text), text) for text in outs]
    return sorted(outs)[-1][1]

if __name__ == "__main__":
    outs = []
    for line in open("data.txt").readlines():
        outs.append(crack_single_byte_xor(codecs.decode(line.strip(), "hex")))
    outs = [(english_score(text), text) for text in outs]
    result = sorted(outs)[-1][1]
    print(result)
    assert result == b"Now that the party is jumping\n"
