#!/usr/bin/env python3.8

import codecs

def fixed_xor(a, b):
    assert len(a) == len(b)
    out = bytearray()
    for i in range(len(a)):
        out.append(a[i] ^ b[i])
    return out

if __name__ == "__main__":
    a = codecs.decode("1c0111001f010100061a024b53535009181c", "hex")
    b = codecs.decode("686974207468652062756c6c277320657965", "hex")
    result = fixed_xor(a, b)
    print(result)
    assert result == codecs.decode("746865206b696420646f6e277420706c6179", "hex")
