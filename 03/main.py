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

if __name__ == "__main__":
    cyphertext = codecs.decode("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736", "hex")
    outs = [single_byte_xor(cyphertext, k) for k in range(256)]
    outs = [(english_score(text), text) for text in outs]
    result = sorted(outs)[-1][1]
    print(result)
    assert result == b"Cooking MC's like a pound of bacon"
