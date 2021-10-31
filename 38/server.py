import random, hashlib, string
from constants import N, g, k
from util import hmac

class Server:
    users = {
            "me@wesleyac.com": "madeline",
            "test@example.com": ''.join(random.choice(string.ascii_letters) for i in range(32))
    }

    def stage0(self, user, A):
        self.salt = random.randint(0,2**128)
        self.x = int(hashlib.sha256(f"{self.salt}.{self.users[user]}".encode()).hexdigest(), 16)
        self.v = pow(g, self.x, N)
        self.b = random.randint(0,N)
        self.B = pow(g, self.b, N)
        self.u = random.randint(0,2**128)
        self.A = A

        return {
            "salt": self.salt,
            "B": self.B,
            "u": self.u
        }

    def stage1(self, client_hmac):
        S = pow((self.A * pow(self.v, self.u, N)), self.b, N)
        K = hashlib.sha256(f"{S}".encode()).hexdigest()
        server_hmac = hmac(K.encode(), f"{self.salt}".encode())
        if server_hmac == client_hmac:
            return "OK"
        else:
            return "ERR"

