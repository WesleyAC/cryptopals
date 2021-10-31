import hashlib

def xor_bytes(i1, i2):
    return bytes(a ^ b for a, b in zip(i1, i2))

def hmac(key, msg):
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    if len(key) < 64:
        key = key + bytes([0] * (64 - len(key)))

    o_key_pad = xor_bytes(key, [0x5c] * 64)
    i_key_pad = xor_bytes(key, [0x36] * 64)

    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + msg).digest()).digest()
