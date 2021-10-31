#!/usr/bin/env python3.8

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

def oracle(plaintext):
    plaintext = plaintext + codecs.decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK", "base64")
    cipher = AES.new(oracle_key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(plaintext, 16))

def outputs_for_prefix(prefix):
    outputs = {}
    for i in range(256):
        outputs[oracle(prefix + bytes([i]))[:len(prefix)+1]] = i
    return outputs

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

    print("---")

    discovered = bytearray([42]*(keysize-1))
    for i in range(0,139):
        blocknum = i // keysize
        prefix = discovered[i:]
        outputs = outputs_for_prefix(prefix)
        cyphertext = oracle(bytes([42]*(keysize-1-(i%keysize))))
        print(chr(outputs[cyphertext[keysize*blocknum:keysize*(blocknum+1)]]), end="")
        discovered.append(outputs[cyphertext[keysize*blocknum:keysize*(blocknum+1)]])
