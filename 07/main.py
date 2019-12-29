#!/usr/bin/env python3

from Crypto.Cipher import AES
import base64, codecs

if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"

    cipher = AES.new(key, AES.MODE_ECB)
    print(codecs.decode(cipher.decrypt(base64.b64decode(open("data.txt").read()))))
