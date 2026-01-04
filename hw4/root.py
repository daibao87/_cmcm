import random
import cmath

def evaluate_poly(coeffs, x):
    """
    使用霍納法 (Horner's Method) 計算多項式的值 P(x)
    coeffs: [c0, c1, ..., cn]
    """
    result = 0
    # 從最高次項開始計算 (倒序遍歷)
    for c in reversed(coeffs):
        result = result * x + c
    return result

def evaluate_derivative(coeffs, x):
    """
    計算多項式導數的值 P'(x)
    P(x) = c0 + c1*x + ... + cn*x^n
    P'(x) = c1 + 2*c2*x + ... + n*cn*x^(n-1)
    """
    result = 0
    n = len(coeffs) - 1
    # 導數係數是 c[i] * i，從最高次項開始
    for i in range(n, 0, -1):
        result = result * x + (coeffs[i] * i)
    return result

def synthetic_division(coeffs, root):
    """
    綜合除法 (Synthetic Division) 用於降次 (Deflation)
    將 P(x) 除以 (x - root)，返回商式係數
    """
    n = len(coeffs) - 1
    new_coeffs = [0] * n # 商式是 n-1 次，係數有 n 個
    
    # 最高次係數直接繼承
    remainder = coeffs[-1]
    new_coeffs[-1] = remainder
    
    # 從次高項往下算
    for i in range(n-2, -1, -1):
        remainder = coeffs[i+1] + remainder * root
        new_coeffs[i] = remainder
        
    return new_coeffs

def find_one_root_newton(coeffs, max_iter=1000, tol=1e-10):
    """
    使用牛頓法在複數平面上尋找單一根
    """
    # 隨機初始化一個複數起點 (避免 0，避免對稱陷阱)
    z = complex(random.random(), random.random())
    
    for _ in range(max_iter):
        p_val = evaluate_poly(coeffs, z)
        
        # 如果值已經夠小，視為找到根
        if abs(p_val) < tol:
            return z
            
        p_deriv = evaluate_derivative(coeffs, z)
        
        # 避免導數為 0 (除以零錯誤)
        if p_deriv == 0:
            # 隨機擾動一下再試
            z += complex(random.random() * 0.1, random.random() * 0.1)
            continue
            
        # 牛頓法迭代公式: z = z - P(z)/P'(z)
        z = z - p_val / p_deriv
        
    return z

def root(c):
    """
    主函數：求 n 次多項式的根
    c: 係數陣列 [c0, c1, ..., cn]
    """
    # 複製一份係數，避免修改原始數據
    current_coeffs = list(c)
    
    # 移除高次項為 0 的情況 (例如 [1, 2, 0, 0] 其實只是 1次多項式)
    while len(current_coeffs) > 0 and current_coeffs[-1] == 0:
        current_coeffs.pop()
        
    n = len(current_coeffs) - 1
    if n < 1:
        return []

    roots = []
    
    # 我們需要找 n 個根
    for _ in range(n):
        # 1. 找到一個根
        r = find_one_root_newton(current_coeffs)
        
        # 2. 修正數值誤差 (如果虚部極小，視為實數)
        if abs(r.imag) < 1e-8:
            r = r.real + 0j
            
        roots.append(r)
        
        # 3. 降次 (Deflation): P(x) <- P(x) / (x - r)
        # 如果只剩常數項就不需要降次了
        if len(current_coeffs) > 2:
            current_coeffs = synthetic_division(current_coeffs, r)
            
    return roots

# --- 測試區 ---

# 例子 1: x^2 - 2x + 1 = 0 (根是 1, 1) -> c = [1, -2, 1]
c1 = [1, -2, 1]
print(f"多項式 1 (x^2 - 2x + 1) 的根: {root(c1)}")

# 例子 2: x^5 - 1 = 0 (5個根) -> c = [-1, 0, 0, 0, 0, 1]
c2 = [-1, 0, 0, 0, 0, 1]
roots_c2 = root(c2)
print(f"\n多項式 2 (x^5 - 1) 的根:")
for r in roots_c2:
    print(f"{r:.2f}") # 格式化輸出以便閱讀

# 例子 3: (x-2)(x-3)(x-4)(x-5)(x-6) 
# 展開後係數很複雜，我們可以測試程式是否能還原這些根
# 這裡簡單測試已知根構建的多項式
# P(x) = x^2 + 1 -> [1, 0, 1] -> 根 i, -i
c3 = [1, 0, 1]
print(f"\n多項式 3 (x^2 + 1) 的根: {root(c3)}")
