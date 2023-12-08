from ECC import ECC, find_Modular_Inverse
from Point import Point
from random import randint

class ECDSA():
    def __init__(self, ECC, d):
        self.ECC = ECC
        self.d = d
        self.Q = ECC.multiply(ECC.G, d)
        if not ECC.check_generator(ECC.G):
            print("Num points: ", ECC.get_num_points())
            raise Exception("Invalid ECC parameters, G is not a generator")
        print("Public Key: ", self.Q)
        print("Private Key: ", self.d)
        print("Num points: ", ECC.get_num_points())

    def get_r(self, k):
        return self.ECC.multiply(self.ECC.G, k).x

    def get_s(self, hash, r, k):
        return (find_Modular_Inverse(k, self.ECC.n) * (hash + self.d * r)) % self.ECC.n

    def sign(self, hash):
        while True:
            k = 2
            r = self.get_r( k)
            if r == 0:
                print("r = 0 with k = ", k)
                continue
            s = self.get_s(hash, r, k)
            if s == 0:
                print("s = 0 with k = ", k)
                continue
            print("Generated K: ", k)
            return r, s

    def verify(self, hash, r, s):
        if r < 1 or r > self.ECC.n or s < 1 or s > self.ECC.n:
            return False
        w = find_Modular_Inverse(s, self.ECC.n)
        print(s)
        print("w: ", w)
        u1 = (hash * w) % self.ECC.n
        u2 = (r * w) % self.ECC.n
        print("u1: ", u1)
        print("u2: ", u2)
        print("u1xG: ", self.ECC.multiply(self.ECC.G, u1))
        print("u2xQ: ", self.ECC.multiply(self.Q, u2))
        P = self.ECC.sum(self.ECC.multiply(self.ECC.G, u1), self.ECC.multiply(self.Q, u2))
        print("P: ", P)
        return r == P.x
    
    def get_public_key(self):
        return self.Q
    
    def get_private_key(self):
        return self.d
    
    def generate_k(self):
        return randint(1, self.ECC.n - 1)

def main():
    m = 1
    curve = ECC(17, 1, 1, Point(0,1))
    d = 1
    ecdsa = ECDSA(curve, d)
    r, s = ecdsa.sign(m)
    print(r, s)
    print(ecdsa.verify(m, r, s))

if __name__ == "__main__":
    main()