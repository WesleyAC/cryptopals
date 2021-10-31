#!/usr/bin/env python3.8

import codecs

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

if __name__ == "__main__":
    text = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    golden = b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    result = codecs.encode(xor_repeat(text, b"ICE"), "hex")
    print(result)
    assert result == golden
