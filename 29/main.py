#!/usr/bin/env python3.8

# this code is..... not so good.
# but i'm tired of thinking about padding, so fuck it, ship it

from sha1 import Sha1Hash
import struct
import os, random

def gen_mac(key, msg):
    return Sha1Hash().update(key + msg).digest()

def check_mac(key, msg, mac):
    return Sha1Hash().update(key + msg).digest() == mac

def gen_padding(l):
    # append the bit '1' to the message
    p = b'\x80'

    # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
    # is congruent to 56 (mod 64)
    p += b'\x00' * ((56 - (l + 1) % 64) % 64)

    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    p += struct.pack(b'>Q', l * 8)

    return p

def gen_padding_good(pl, tl):
    # append the bit '1' to the message
    p = b'\x80'

    # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
    # is congruent to 56 (mod 64)
    p += b'\x00' * ((56 - (pl + 1) % 64) % 64)

    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    p += struct.pack(b'>Q', tl * 8)

    return p

def get_registers(h):
    return (
        int.from_bytes(h[0:4], "big"),
        int.from_bytes(h[4:8], "big"),
        int.from_bytes(h[8:12], "big"),
        int.from_bytes(h[12:16], "big"),
        int.from_bytes(h[16:20], "big"),
    )

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff
    
def sha1(message, h):
    """SHA-1 Hashing Function
    A custom SHA-1 hashing function implemented entirely in Python.
    Arguments:
        message: The input message string to hash.
    Returns:
        A hex SHA-1 digest of the input message.
    """
    # Initialize variables:
    h0 = h[0]
    h1 = h[1]
    h2 = h[2]
    h3 = h[3]
    h4 = h[4]

    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, 
                            a, _left_rotate(b, 30), c, d)

        # Add this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff 
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    # Produce the final hash value (big-endian):
    return b''.join(struct.pack(b'>I', h) for h in (h0, h1, h2, h3, h4))

if __name__ == "__main__":
    msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    key = os.urandom(random.randint(5, 20))
    mac = gen_mac(key, msg)
    assert check_mac(key, msg, mac)

    for keylen in range(1, 32):
        append_text = b";admin=true"
        new_mac = sha1(
            append_text +
            gen_padding_good(len(append_text), keylen + len(msg) + len(append_text) + len(gen_padding(len(msg) + keylen))),
            get_registers(mac)
        )
        new_msg = msg + gen_padding(len(msg) + keylen) + b";admin=true"
        if check_mac(key, new_msg, new_mac):
            print(new_mac)
            print(new_msg)
            print(f"keylen: {keylen}")
