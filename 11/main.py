#!/usr/bin/env python3.8

import os, random
from Crypto.Cipher import AES

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def oracle(plaintext):
    key = os.urandom(16)
    plaintext = os.urandom(random.randint(5,10)) + plaintext + os.urandom(random.randint(5,10))
    mode = AES.MODE_ECB if random.random() > 0.5 else AES.MODE_CBC
    print("ECB" if mode == AES.MODE_ECB else "CBC", end=" ")
    cipher = AES.new(key, mode)
    return cipher.encrypt(pkcs7_pad(plaintext, 16))

if __name__ == "__main__":
    for _ in range(10):
        cyphertext = oracle(bytes([42]*16*16))
        chunked = list(chunks(cyphertext, 16))
        if len(chunked) != len(set(chunked)):
            print("ECB")
        else:
            print("CBC")
