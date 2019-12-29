#!/usr/bin/env python3

from Crypto.Cipher import AES
import base64, codecs

# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def xor_repeat(plaintext, key):
    out = bytearray()
    for i in range(len(plaintext)):
        out.append(plaintext[i] ^ key[i % len(key)])
    return out

def cbc_decrypt(cyphertext, key, iv):
    cyphertext = list(chunks(cyphertext, len(key)))
    out = bytearray()
    for i in range(len(cyphertext)):
        cipher = AES.new(key, AES.MODE_ECB)
        xor = cyphertext[i-1] if i > 0 else iv
        pt = xor_repeat(cipher.decrypt(cyphertext[i]), xor)
        out += pt
    return out

if __name__ == "__main__":
    cyphertext = codecs.decode(open("data.txt").read().encode(), "base64")
    print(codecs.decode(cbc_decrypt(cyphertext, b"YELLOW SUBMARINE", [0]*16)))
