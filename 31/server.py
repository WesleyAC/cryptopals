#!/usr/bin/env python3.8

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import codecs, hashlib, os, time

def xor_bytes(i1, i2):
    return bytes(a ^ b for a, b in zip(i1, i2))

def hmac(key, msg):
    if len(key) > 64:
        key = hashlib.sha1(key).digest()
    if len(key) < 64:
        key = key + bytes([0] * (64 - len(key)))

    o_key_pad = xor_bytes(key, [0x5c] * 64)
    i_key_pad = xor_bytes(key, [0x36] * 64)

    return hashlib.sha1(o_key_pad + hashlib.sha1(i_key_pad + msg).digest()).digest()

secret_key = os.urandom(64)

def insecure_compare(a, b):
    if len(a) != len(b): return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
        time.sleep(0.05)
    return True

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        f = q["file"][0].encode()
        sig = q["signature"][0].encode()
        if insecure_compare(hmac(secret_key, f), codecs.decode(sig, "hex")):
            self.send_response(200)
        else:
            self.send_response(500)

        self.end_headers()
        return

if __name__ == '__main__':
    assert codecs.encode(hmac(b"key", b"The quick brown fox jumps over the lazy dog"), "hex") == b"de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9"
    print(codecs.encode(hmac(secret_key, b"test"), "hex"))
    server = HTTPServer(('localhost', 9000), RequestHandler)
    server.serve_forever()
