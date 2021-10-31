import random, hashlib, os
from constants import N, g, k
from server import Server
from util import hmac

class Mitm:
    server = Server()

    def stage0(self, user, A):
        self.user = user
        self.A = A

        self.b = random.randint(0,N)
        self.B = pow(g, self.b, N)

        response0 = self.server.stage0(user, A)

        self.salt = response0["salt"]
        self.real_B = response0["B"]
        self.u = response0["u"]

        return {
                "salt": self.salt,
                "B": self.B,
                "u": self.u,
        }

    def stage1(self, hmac):
        self.client_hmac = hmac
        return self.server.stage1(hmac)

    def crack_password(self):
        passwords_file = os.path.join(os.path.dirname(__file__), "10-million-password-list-top-10000.txt")
        for password in open(passwords_file).readlines():
            password = password.strip()
            x = int(hashlib.sha256(f"{self.salt}.{password}".encode()).hexdigest(), 16)
            v = pow(g, x, N)
            S = pow((self.A * pow(v, self.u, N)), self.b, N)
            K = hashlib.sha256(f"{S}".encode()).hexdigest()
            test_hmac = hmac(K.encode(), f"{self.salt}".encode())
            if test_hmac == self.client_hmac:
                print(f"found password: {password}")
