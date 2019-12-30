#!/usr/bin/env python3

import codecs, requests, time

if __name__ == "__main__":
    msg = "test"
    test_hmac = bytearray([0]*20)
    for i in range(20):
        for b in range(256):
            test_hmac[i] = b
            signature = codecs.encode(test_hmac, "hex")
            start = time.time()
            requests.get("http://localhost:9000/test", params={"file": msg, "signature": signature})
            end = time.time()
            if end - start > (i+1)*0.05:
                break
    print(codecs.encode(test_hmac, "hex"))
