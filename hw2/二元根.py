import cmath
p = 1
q = -2
r = 3
def find_roots(x, y, z):
    delta = y ** 2 - 4 * x * z
    if delta != 0:
        sol1 = (-y + cmath.sqrt(delta)) / (2 * x)
        sol2 = (-y - cmath.sqrt(delta)) / (2 * x)
    else:
        sol1 = -y / (2 * x)
        sol2 = sol1
    return sol1, sol2
ans1, ans2 = find_roots(p, q, r)
print("第一根 =", ans1)
print("第二根 =", ans2)
