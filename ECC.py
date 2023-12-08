from math import gcd
import Point
class ECC:
    def __init__(self, p, a, b, G):
        if 4 * pow(a, 3) + 27 * pow(b, 2) % p == 0:
            raise Exception("Invalid ECC parameters, 4a^3 + 27b^2 = 0")
        self.p = p
        self.a = a
        self.b = b
        if type(G) != Point:
            raise Exception("Invalid ECC parameters, G should be a point")
        if G.y*G.y != pow(G.x, 3) + a * G.x + b or G.x >= p or G.y >= p or G.x < 0 or G.y < 0:
            raise Exception("Invalid ECC parameters, G is not on the curve")
        self.G = G
        self.points = []
        self.points.append(Point(0, 0))
    
    def add_point(self, x, y):
        self.points.append(Point(x, y))

    
    def sum(self, p1, p2):
        if p1 == self.points[0]:
            return p2
        elif p2 == self.points[0]:
            return p1
        elif p1.x == p2.x:
            return self.points[0]
        elif p1 == p2:
            m = (3 * pow(p1.x, 2) + self.a) * find_Modular_Inverse(2 * p1.y, self.p)
            x = (m * m - 2 * p1.x) % self.p
            y = (m * (p1.x - x) - p1.y) % self.p
            return Point(x, y)
        else:
            m = (p2.y - p1.y) * find_Modular_Inverse(p2.x - p1.x, self.p)
            x = (m * m - p1.x - p2.x) % self.p
            y = (m * (p1.x - x) - p1.y) % self.p
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

def find_Modular_Inverse(a, m):
    if gcd(a, m) != 1:
        return None
    else:
        return pow(a, -1, m)
