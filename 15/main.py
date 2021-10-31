#!/usr/bin/env python3.8

def check_pkcs7(s):
    strip_amount = s[-1]
    if set(s[len(s) - strip_amount:]) != set([strip_amount]):
        raise ValueError("bad padding")
    return s[:-strip_amount]

if __name__ == "__main__":
    good = check_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04")
    print(good)
    assert good == b"ICE ICE BABY"
    try: 
        check_pkcs7(b"ICE ICE BABY\x05\x05\x05\x05")
    except ValueError as e:
        assert str(e) == "bad padding"
    try: 
        check_pkcs7(b"ICE ICE BABY\x01\x02\x03\x04")
    except ValueError as e:
        assert str(e) == "bad padding"
