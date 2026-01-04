import cmath

def root3(a, b, c, d):

    # 確保輸入為複數型態，避免 Python 整數除法或精度問題
    a, b, c, d = complex(a), complex(b), complex(c), complex(d)
    
    # 處理特殊情況：若 a=0，則退化為二次方程式 (bx^2 + cx + d = 0)
    if a == 0:
        if b == 0:
            # 線性方程 cx + d = 0
            return (-d/c,) if c != 0 else "無解或無限多解"
        # 二次方程公式
        D = cmath.sqrt(c**2 - 4*b*d)
        return ((-c + D) / (2*b), (-c - D) / (2*b))

    # 1. 計算 Delta_0 和 Delta_1
    delta0 = b**2 - 3*a*c
    delta1 = 2*b**3 - 9*a*b*c + 27*a**2*d

    # 2. 計算 C
    # 這裡需要計算平方根，可能會產生複數
    inner_sqrt = cmath.sqrt(delta1**2 - 4*delta0**3)
    
    # 計算 C 的核心部分：(Delta_1 +/- inner_sqrt) / 2
    # 為了數值穩定性，如果 C 計算出來是 0 (這會導致後面除以零)，我們應該改變正負號
    # 但數學上，一般取正號即可，除非 delta1 和 inner_sqrt 剛好抵消
    C_cubed = (delta1 + inner_sqrt) / 2
    
    # 若取加號導致 C_cubed 為 0，則嘗試減號 (這種情況發生在三重根或特定條件)
    if C_cubed == 0:
        C_cubed = (delta1 - inner_sqrt) / 2

    # 取立方根 (注意：Python 的 **(1/3) 會回傳主值)
    C = C_cubed**(1/3)

    # 特殊情況：如果經過上述步驟 C 仍然是 0 (代表 delta0 = 0 且 delta1 = 0)，則是三重實根
    if C == 0:
        x = -b / (3*a)
        return (x, x, x)

    # 3. 計算三個根
    # 定義 xi (1 的複數立方根: (-1 + sqrt(3)i) / 2)
    xi = complex(-0.5, cmath.sqrt(3).real / 2)
    
    # 根據維基百科公式計算 x_k
    # x_k = -1/(3a) * (b + xi^k * C + delta0 / (xi^k * C))
    
    roots = []
    xi_powers = [1, xi, xi**2] # 對應 k=0, 1, 2
    
    for k_xi in xi_powers:
        term = b + k_xi * C + delta0 / (k_xi * C)
        root = -1 / (3*a) * term
        roots.append(root)

    return tuple(roots)

# --- 測試範例 ---

# 範例 1: x^3 - 6x^2 + 11x - 6 = 0 (根應該是 1, 2, 3)
print("範例 1 (實根 1, 2, 3):")
r1 = root3(1, -6, 11, -6)
for r in r1:
    print(f"{r:.2f}") 
    # 註：輸出可能會帶有極小的虛部 (如 1.00+0.00j)，這是浮點數運算的正常現象

print("-" * 20)

# 範例 2: x^3 - 1 = 0 (根是 1 和兩個複數根)
print("範例 2 (x^3 - 1 = 0):")
r2 = root3(1, 0, 0, -1)
for r in r2:
    print(f"{r:.2f}")

print("-" * 20)

# 範例 3: x^3 + x + 1 = 0 (一個實根，兩個複數根)
print("範例 3 (x^3 + x + 1 = 0):")
r3 = root3(1, 0, 1, 1)
for r in r3:
    print(f"{r:.2f}")
