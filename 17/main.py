#!/usr/bin/env python3.8

import codecs, os, random
from Crypto.Cipher import AES

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

def check_pkcs7(s):
    strip_amount = s[-1]
    if strip_amount > len(s) or set(s[len(s) - strip_amount:]) != set([strip_amount]):
        raise ValueError("bad padding")
    return s[:-strip_amount]

random_key = os.urandom(16)

def encrypt():
    plaintext = codecs.decode(random.choice(open('data.txt').read().splitlines()).encode(), "base64")
    iv = os.urandom(16)
    cipher = AES.new(random_key, AES.MODE_CBC, iv)
    return (cipher.encrypt(pkcs7_pad(plaintext, len(random_key))), iv)

def decrypt(ciphertext, iv):
    cipher = AES.new(random_key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    try:
        check_pkcs7(plaintext)
        return True
    except:
        return False

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def crack_blocks(b1, b2, skip):
    known_intermediate = bytearray([])
    out = bytearray([])
    for p in range(16):
        for i in range(256):
            if decrypt(b2, b1[:15-p] + bytes([i]) + bytearray(map(lambda e: e ^ p+1, known_intermediate))):
                if skip == 0:
                    known_intermediate.insert(0, i ^ p+1)
                    out.insert(0, b1[15-p] ^ (i ^ p+1))
                    break
                else:
                    skip -= 1
    return out

if __name__ == "__main__":
    ciphertext, iv = encrypt()
    all_together = iv + ciphertext
    for i in range((len(all_together)//16)-1):
        skip = 0
        while True:
            try:
                print(codecs.decode(crack_blocks(all_together[i*16:(i+1)*16], all_together[(i+1)*16:(i+2)*16], skip)), end="")
            except ValueError:
                skip += 1
                continue
            break

