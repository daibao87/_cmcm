import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, factor, center=None):
        if center is None: center = Point(0, 0)
        self.x = center.x + (self.x - center.x) * factor
        self.y = center.y + (self.y - center.y) * factor

    def rotate(self, angle_deg, center=None):
        if center is None: center = Point(0, 0)
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        tx = self.x - center.x
        ty = self.y - center.y
        
        self.x = center.x + (tx * cos_a - ty * sin_a)
        self.y = center.y + (tx * sin_a + ty * cos_a)

class Line:
    def __init__(self, p1, p2):
        self.p1 = Point(p1.x, p1.y) 
        self.p2 = Point(p2.x, p2.y)

    def get_coeffs(self):
        A = self.p1.y - self.p2.y
        B = self.p2.x - self.p1.x
        C = A * self.p1.x + B * self.p1.y
        return A, B, C

    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"

    def translate(self, dx, dy):
        self.p1.translate(dx, dy)
        self.p2.translate(dx, dy)

    def scale(self, factor, center=None):
        self.p1.scale(factor, center)
        self.p2.scale(factor, center)

    def rotate(self, angle_deg, center=None):
        self.p1.rotate(angle_deg, center)
        self.p2.rotate(angle_deg, center)

class Circle:
    def __init__(self, center, radius):
        self.center = Point(center.x, center.y)
        self.radius = radius

    def __repr__(self):
        return f"Circle(Center={self.center}, r={self.radius:.2f})"

    def translate(self, dx, dy):
        self.center.translate(dx, dy)

    def scale(self, factor, center=None):

        self.radius *= factor
        if center:
            self.center.scale(factor, center)

    def rotate(self, angle_deg, center=None):
      
        if center:
            self.center.rotate(angle_deg, center)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.points = [Point(p1.x, p1.y), Point(p2.x, p2.y), Point(p3.x, p3.y)]

    def __repr__(self):
        return f"Triangle({self.points[0]}, {self.points[1]}, {self.points[2]})"

    def translate(self, dx, dy):
        for p in self.points: p.translate(dx, dy)

    def scale(self, factor, center=None):

        if center is None:
            cx = sum(p.x for p in self.points) / 3
            cy = sum(p.y for p in self.points) / 3
            center = Point(cx, cy)
        for p in self.points: p.scale(factor, center)

    def rotate(self, angle_deg, center=None):

        if center is None:
            cx = sum(p.x for p in self.points) / 3
            cy = sum(p.y for p in self.points) / 3
            center = Point(cx, cy)
        for p in self.points: p.rotate(angle_deg, center)

def intersect_line_line(l1, l2):
    A1, B1, C1 = l1.get_coeffs()
    A2, B2, C2 = l2.get_coeffs()
    det = A1 * B2 - A2 * B1
    if abs(det) < 1e-9:
        return None 
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det
    return Point(x, y)

def get_perpendicular_foot(p, line):
    ax, ay = line.p1.x, line.p1.y
    bx, by = line.p2.x, line.p2.y
    px, py = p.x, p.y

    ab_x, ab_y = bx - ax, by - ay
    ap_x, ap_y = px - ax, py - ay

    denom = ab_x**2 + ab_y**2
    if denom == 0: return line.p1 
    
    k = (ap_x * ab_x + ap_y * ab_y) / denom
    hx = ax + k * ab_x
    hy = ay + k * ab_y
    return Point(hx, hy)

def intersect_line_circle(line, circle):

    d = Point(line.p2.x - line.p1.x, line.p2.y - line.p1.y)
    f = Point(line.p1.x - circle.center.x, line.p1.y - circle.center.y)

    a = d.x**2 + d.y**2
    b = 2 * (f.x * d.x + f.y * d.y)
    c = (f.x**2 + f.y**2) - circle.radius**2

    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return [] 
    
    discriminant = math.sqrt(discriminant)
    t1 = (-b - discriminant) / (2*a)
    t2 = (-b + discriminant) / (2*a)
    
    sol1 = Point(line.p1.x + t1*d.x, line.p1.y + t1*d.y)
    if abs(discriminant) < 1e-9:
        return [sol1] 
    
    sol2 = Point(line.p1.x + t2*d.x, line.p1.y + t2*d.y)
    return [sol1, sol2]

def intersect_circle_circle(c1, c2):
    d = c1.center.distance_to(c2.center)

    if d > c1.radius + c2.radius or d < abs(c1.radius - c2.radius) or d == 0:
        return [] 

    a = (c1.radius**2 - c2.radius**2 + d**2) / (2 * d)
    h = math.sqrt(max(0, c1.radius**2 - a**2))

    x2 = c1.center.x + a * (c2.center.x - c1.center.x) / d
    y2 = c1.center.y + a * (c2.center.y - c1.center.y) / d
    
    x3_1 = x2 + h * (c2.center.y - c1.center.y) / d
    y3_1 = y2 - h * (c2.center.x - c1.center.x) / d
    x3_2 = x2 - h * (c2.center.y - c1.center.y) / d
    y3_2 = y2 + h * (c2.center.x - c1.center.x) / d
    
    return [Point(x3_1, y3_1), Point(x3_2, y3_2)]

print("--- 幾何計算展示 ---")
# 1. 兩直線交點
l1 = Line(Point(0, 0), Point(4, 4))
l2 = Line(Point(0, 4), Point(4, 0))
inter_ll = intersect_line_line(l1, l2)
print(f"兩直線交點: {inter_ll}")

# 2. 直線與圓交點
circ = Circle(Point(2, 2), 2)
inter_lc = intersect_line_circle(l1, circ)
print(f"直線與圓交點: {inter_lc}")

# 3. 兩圓交點
circ2 = Circle(Point(4, 2), 2)
inter_cc = intersect_circle_circle(circ, circ2)
print(f"兩圓交點: {inter_cc}")

print("\n--- 畢氏定理驗證 ---")

line_base = Line(Point(0, 0), Point(10, 0)) # x軸
point_p = Point(3, 4)

foot_h = get_perpendicular_foot(point_p, line_base)
print(f"線外一點 P: {point_p}")
print(f"直線上一點 (垂足 H): {foot_h}")

point_a = line_base.p1 

a = point_p.distance_to(foot_h) # 股 (垂線長)
b = foot_h.distance_to(point_a) # 股 (直線上距離)
c = point_p.distance_to(point_a) # 斜邊

print(f"三角形邊長: a(PH)={a}, b(HA)={b}, c(PA)={c}")
print(f"驗證: a^2 + b^2 = {a**2 + b**2:.2f}")
print(f"驗證: c^2       = {c**2:.2f}")
is_pythagoras = abs((a**2 + b**2) - c**2) < 1e-9
print(f"畢氏定理成立: {is_pythagoras}")

print("\n--- 幾何變換 (平移/旋轉/縮放) ---")
tri = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
print(f"原始三角形: {tri}")

tri.translate(1, 1)
print(f"平移 (1,1) 後: {tri}")

tri.scale(2) # 預設繞重心放大
print(f"放大 2 倍後: {tri}")

tri.rotate(90) # 預設繞重心旋轉
print(f"旋轉 90 度後: {tri}")
