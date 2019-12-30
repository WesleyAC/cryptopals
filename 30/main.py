#!/usr/bin/env python3

import codecs, os, random
from md4 import md4

from struct import pack
from binascii import hexlify

def make_words(byte_array):
    res = []

    for i in range(0, len(byte_array), 4):
        index = i//4
        res.append(byte_array[i+3])
        res[index] = (res[index] << 8) | byte_array[i+2]
        res[index] = (res[index] << 8) | byte_array[i+1]
        res[index] = (res[index] << 8) | byte_array[i]

    return res
        
def md4_mod(message, A, B, C, D):
    """
    https://tools.ietf.org/html/rfc1320
    """

    message = [c for c in message]

    # define F, G, and H
    def F(x,y,z): return ((x & y) | ((~x) & z))
    def G(x,y,z): return (x & y) | (x & z) | (y & z)
    def H(x,y,z): return x ^ y ^ z

    # round functions
    def FF(a,b,c,d,k,s): return ROL((a + F(b,c,d) + X[k]) & 0xFFFFFFFF, s)
    def GG(a,b,c,d,k,s): return ROL((a + G(b,c,d) + X[k] + 0x5A827999) & 0xFFFFFFFF, s)
    def HH(a,b,c,d,k,s): return ROL((a + H(b,c,d) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, s)

    # define a 32-bit left-rotate function (<<< in the RFC)
    def ROL(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32-n))

    # turn the padded message into a list of 32-bit words
    M = make_words(message)
        
    # process each 16 word (64 byte) block
    for i in range(0, len(M), 16):
        X = M[i:i+16]

        # save the current values of the registers
        AA = A
        BB = B
        CC = C
        DD = D

        # round 1

        # perform the 16 operations
        A = FF(A,B,C,D,0,3)
        D = FF(D,A,B,C,1,7)
        C = FF(C,D,A,B,2,11)
        B = FF(B,C,D,A,3,19)

        A = FF(A,B,C,D,4,3)
        D = FF(D,A,B,C,5,7)
        C = FF(C,D,A,B,6,11)
        B = FF(B,C,D,A,7,19)

        A = FF(A,B,C,D,8,3)
        D = FF(D,A,B,C,9,7)
        C = FF(C,D,A,B,10,11)
        B = FF(B,C,D,A,11,19)

        A = FF(A,B,C,D,12,3)
        D = FF(D,A,B,C,13,7)
        C = FF(C,D,A,B,14,11)
        B = FF(B,C,D,A,15,19)

        # round 2

        # perform the 16 operations
        A = GG(A,B,C,D,0,3)
        D = GG(D,A,B,C,4,5)
        C = GG(C,D,A,B,8,9)
        B = GG(B,C,D,A,12,13)

        A = GG(A,B,C,D,1,3)
        D = GG(D,A,B,C,5,5)
        C = GG(C,D,A,B,9,9)
        B = GG(B,C,D,A,13,13)

        A = GG(A,B,C,D,2,3)
        D = GG(D,A,B,C,6,5)
        C = GG(C,D,A,B,10,9)
        B = GG(B,C,D,A,14,13)

        A = GG(A,B,C,D,3,3)
        D = GG(D,A,B,C,7,5)
        C = GG(C,D,A,B,11,9)
        B = GG(B,C,D,A,15,13)

        # round 3

        A = HH(A,B,C,D,0,3)
        D = HH(D,A,B,C,8,9)
        C = HH(C,D,A,B,4,11)
        B = HH(B,C,D,A,12,15)

        A = HH(A,B,C,D,2,3)
        D = HH(D,A,B,C,10,9)
        C = HH(C,D,A,B,6,11)
        B = HH(B,C,D,A,14,15)

        A = HH(A,B,C,D,1,3)
        D = HH(D,A,B,C,9,9)
        C = HH(C,D,A,B,5,11)
        B = HH(B,C,D,A,13,15)

        A = HH(A,B,C,D,3,3)
        D = HH(D,A,B,C,11,9)
        C = HH(C,D,A,B,7,11)
        B = HH(B,C,D,A,15,15)

        # increment by previous values
        A =  ((A + AA) & 0xFFFFFFFF)
        B =  ((B + BB) & 0xFFFFFFFF)
        C =  ((C + CC) & 0xFFFFFFFF)
        D =  ((D + DD) & 0xFFFFFFFF)

    return A.to_bytes(4, 'little') + B.to_bytes(4, 'little') + C.to_bytes(4, 'little') + D.to_bytes(4, 'little')

def pad(pl, tl):
    p = [0x80]

    mod_length = (pl + 1) % 64
    # padding to 448 % 512 bits (56 % 64 byte)
    if mod_length < 56:
        p += [0x00] * (56 - mod_length)
    else:
        p += [0x00] * (120 - mod_length)

    # add the length as a 64 bit big endian, use lower order bits if length overflows 2^64
    length = [c for c in pack('>Q', (tl * 8) & 0xFFFFFFFFFFFFFFFF)]

    # add the two words least significant first
    p.extend(length[::-1])

    return bytes(p)

def get_regs(h):
    return (
        int.from_bytes(h[0:4], "little"),
        int.from_bytes(h[4:8], "little"),
        int.from_bytes(h[8:12], "little"),
        int.from_bytes(h[12:16], "little"),
    )

def check_mac(key, msg, mac):
    return md4(key + msg) == mac

if __name__ == "__main__":
    key = os.urandom(random.randint(3, 20))
    msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    mac = md4(key + msg)
    A, B, C, D = get_regs(mac)

    append_text = b";admin=true"

    for keylen in range(2, 30):
        new_mac = md4_mod(
            append_text +
            pad(
                len(append_text),
                keylen + len(msg) + len(pad(keylen + len(msg), keylen + len(msg))) + len(append_text)
            ),
            A, B, C, D
        )
        new_msg = msg + pad(len(msg) + keylen, len(msg) + keylen) + append_text
        if check_mac(key, new_msg, new_mac):
            print(codecs.encode(new_mac, 'hex'))
            print(new_msg)
            print(f"keylen: {keylen}")
            
