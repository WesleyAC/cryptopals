#!/usr/bin/env python3

import os, random, codecs
from Crypto.Cipher import AES

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

oracle_key = os.urandom(16)
random_prefix = os.urandom(random.randint(17, 50))

def oracle(plaintext):
    plaintext = random_prefix + plaintext + codecs.decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK", "base64")
    cipher = AES.new(oracle_key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(plaintext, 16))

if __name__ == "__main__":
    last_output_size = None
    keysize = None
    i = 1
    while True:
        i += 1
        new_output_size = len(oracle(bytes([42]*i)))
        if last_output_size is not None and new_output_size != last_output_size:
            keysize = new_output_size - last_output_size
            break
        last_output_size = new_output_size
    print(f"key size: {keysize}")

    cyphertext = oracle(bytes([42]*16*16))
    chunked = list(chunks(cyphertext, 16))
    if len(chunked) != len(set(chunked)):
        print("mode: ECB")
    else:
        print("mode: CBC")

    i = 1
    while True:
        i += 1
        out = list(chunks(oracle(bytes([42]*i)), keysize))
        if len(out) != len(set(out)):
            dup = [i for i,c in enumerate(out) if out.count(c) > 1][0]
            prefix_len = (dup * keysize) - (i % keysize)
            break

    print(f"prefix len: {prefix_len}")
    print("---")

    known = bytearray()
    for i in range(139):
        wedge = bytearray([42]*(keysize + keysize - (prefix_len%keysize) - 1 - (i % keysize)))
        strip_amount = prefix_len + len(wedge) + len(known) + 1
        cyphertext = oracle(wedge)[:strip_amount]
        for c in range(256):
            if oracle(wedge + known + bytes([c]))[:strip_amount] == cyphertext:
                print(chr(c), end="")
                known.append(c)
                break
