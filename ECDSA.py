from ECC import ECC, find_Modular_Inverse
from Point import Point
from random import randint

class ECDSA():
    def __init__(self, ECC, d):
        self.ECC = ECC
        self.d = d
        self.Q = ECC.multiply(ECC.G, d)
        self.order = ECC.get_num_points()
        print("Public Key: ", self.Q)
        print("Private Key: ", self.d)
        print("Order: ", self.order)

    def get_r(self, k):
        return self.ECC.multiply(self.ECC.G, k).x % self.order

    def get_s(self, hash, r, k):
        return (find_Modular_Inverse(k, self.order) * (hash + self.d * r)) % self.order

    def sign(self, hash):
        while True:
            k = self.generate_k()
            if extendedEuclid(k, self.order) == False:
                continue
            r = self.get_r( k)
            if r == 0:
                print("r = 0 with k = ", k)
                continue
            s = self.get_s(hash, r, k)
            if s == 0 or extendedEuclid(s, self.order) == False:
                print("s = 0 or s^-1 does not exist with k = ", k)
                continue
            print("Generated K: ", k)
            return r, s

    def verify(self, hash, r, s):
        if r < 1 or r > self.order or s < 1 or s > self.order:
            return False
        w = find_Modular_Inverse(s, self.order)
        print("w: ", w, "\ns: ", s, "\norder: ", self.order)
        u1 = (hash * w) % self.order
        u2 = (r * w) % self.order
        print("u1: ", u1)
        print("u2: ", u2)
        print("u1xG: ", self.ECC.multiply(self.ECC.G, u1))
        print("u2xQ: ", self.ECC.multiply(self.Q, u2))
        P = self.ECC.sum(self.ECC.multiply(self.ECC.G, u1), self.ECC.multiply(self.Q, u2))
        print("P: ", P)
        print("Expected r = ", r, "Actual r = ", P.x)
        return r == P.x
    
    def get_public_key(self):
        return self.Q
    
    def get_private_key(self):
        return self.d
    
    def generate_k(self):
        return randint(1, self.order - 1)

def extendedEuclid(inverse, mod):
    A=(1,0,mod)
    B=(0,1,inverse%mod)
    while True:
        if B[2]==0:
            return False
        if B[2]==1:
            return B[1]
        Q=A[2]//B[2]
        C=((A[0]-Q*B[0])%mod,(A[1]-Q*B[1])%mod,(A[2]-Q*B[2])%mod)
        A=B
        B=C



def main():
    m = 1
    curve = ECC(23, 1, 1, Point(7,11))
    d = 1
    ecdsa = ECDSA(curve, d)
    r, s = ecdsa.sign(m)
    print(r, s)
    print(ecdsa.verify(m, r, s))

if __name__ == "__main__":
    main()