from math import gcd
from Point import Point
class ECC:
    def __init__(self, n, a, b, G):
        if (4 * pow(a, 3) + 27 * pow(b, 2)) % n == 0:
            raise Exception("Invalid ECC parameters, 4a^3 + 27b^2 = 0")
        self.n = n
        self.a = a
        self.b = b
        if not isinstance(G, Point):
            raise Exception("Invalid ECC parameters, G should be a point")
        if G.y*G.y % n != (pow(G.x, 3) + a * G.x + b) % n or G.x >= n or G.y >= n or G.x < 0 or G.y < 0:
            raise Exception("Invalid ECC parameters, G is not on the curve")
        
        
        self.G = G
        self.points = []
        self.points.append(Point(0, 0))
        self.order = self.get_order()
    
    
    def get_num_points(self):
        points = []
        for y in range(self.n):
            for x in range(self.n):
                if y*y % self.n == (pow(x, 3) + self.a * x + self.b) % self.n:
                    if (x,y) not in points:
                        points.append((x,y))
        points.append((0,0))
        points.sort()
        print("Points: ", points)
        return len(points)
    
    def sum(self, p1, p2):
        if p1.x == 0 and p1.y == 0:
            return p2
        elif p2.x == 0 and p2.y == 0:
            return p1
        elif p1.x == p2.x and p1.y == p2.y:
            print("Doubling point: ", p1)
            m = (3 * pow(p1.x, 2) + self.a) * find_Modular_Inverse((2 * p1.y)%self.n, self.n)
            x = (m * m - 2 * p1.x) % self.n
            y = (m * (p1.x - x) - p1.y) % self.n
            if find_Modular_Inverse(2 * p1.y, self.n)==0:
                return Point(0, 0)
            print("Result: ", Point(x, y))
            return Point(x, y)
        else:
            if p1.x == p2.x and p1.y == -p2.y:
                return Point(0, 0)
            m = (p2.y - p1.y) * find_Modular_Inverse((p2.x - p1.x)%self.n, self.n)
            x = (m * m - p1.x - p2.x) % self.n
            y = (m * (p1.x - x) - p1.y) % self.n
            if find_Modular_Inverse(p2.x - p1.x, self.n)==0:
                return Point(0, 0)
            return Point(x, y)

    def multiply(self, point, d):
        if d == 0:
            return self.points[0]
        elif d == 1:
            return point
        else:
            temp = point
            for i in range(1, d):
                temp = self.sum(point, temp)
            return temp
    
    
    def get_inverse(self, point):
        return Point(point.x, -point.y)
    
    def get_order(self):
        order = 0
        temp = self.G
        while temp.x != 0 or temp.y != 0:
            order += 1
            temp = self.sum(temp, self.G)
        return order + 1

def find_Modular_Inverse(a, m):
    if gcd(a, m) != 1:
        return 0
    else:
        return extendedEuclid(a, m)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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