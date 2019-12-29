#!/usr/bin/env python3

def pkcs7_pad(text, blocksize):
    padding = blocksize - (len(text) % blocksize)
    return text + bytes([padding])*padding

if __name__ == "__main__":
    result = pkcs7_pad(b"YELLOW SUBMARINE", 20)
    print(result)
    print(pkcs7_pad(b"0123456789abcdef_", 16))
    assert result == b"YELLOW SUBMARINE\x04\x04\x04\x04"
