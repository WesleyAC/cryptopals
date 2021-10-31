import random, hashlib, string
from constants import N, g, k

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

users = {
        "me@wesleyac.com": "hunter2",
        "test@example.com": ''.join(random.choice(string.ascii_letters) for i in range(32))
}

class Server:
    def stage0(self, email, A):
        self.salt = random.randint(0,2**128)
        self.v = pow(g, int(hashlib.sha256(f"{self.salt}.{users[email]}".encode()).hexdigest(), 16), N)
        self.A = A
        self.b = random.randint(0,N)
        self.B = k*self.v + pow(g, self.b, N)
        return {
            "salt": self.salt,
            "B": self.B,
        }

    def stage1(self, client_hmac):
        u = int(hashlib.sha256(f"{self.A}.{self.B}".encode()).hexdigest(), 16)
        S = pow((self.A * pow(self.v, u, N)), self.b, N)
        K = hashlib.sha256(f"{S}".encode()).hexdigest()
        correct_hmac = hmac(K.encode(), f"{self.salt}".encode())

        return "OK" if client_hmac == correct_hmac else "ERR"
