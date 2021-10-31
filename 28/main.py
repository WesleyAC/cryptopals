#!/usr/bin/env python3.8

from sha1 import Sha1Hash

def gen_mac(key, msg):
    return Sha1Hash().update(key + msg).digest()

def check_mac(key, msg, mac):
    return Sha1Hash().update(key + msg).digest() == mac

if __name__ == "__main__":
    msg = b"hello!"
    key = b"foobar"
    mac = gen_mac(key, msg)
    print(mac)
    assert check_mac(key, msg, mac)
    assert not check_mac(key, b"something else", mac)
