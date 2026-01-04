import numpy as np
from collections import Counter

def solve_ode_general(coefficients):
    """
    求解常係數齊次常微分方程 (ODE)。
    輸入: coefficients (list) - 從高階到低階的係數，例如 y'' - 3y' + 2y = 0 -> [1, -3, 2]
    輸出: str - 通解的字串表達式
    """
    
    roots = np.roots(coefficients)
    

    decimals = 5 
    cleaned_roots = []
    for r in roots:
        real_part = round(r.real, decimals)
        imag_part = round(r.imag, decimals)
        # 如果虛部極小，視為實數
        if abs(imag_part) == 0:
            cleaned_roots.append(real_part)
        else:
            cleaned_roots.append(complex(real_part, imag_part))

    root_counts = Counter(cleaned_roots)
    
    # 為了輸出的順序一致性，我們對根進行排序 (實數優先，複數其次)
    unique_roots = sorted(root_counts.keys(), key=lambda x: (x.imag, x.real))
    
    terms = []
    C_index = 1 # 常數項計數器 (C_1, C_2...)
    
    processed_conjugates = set() # 用來記錄已處理過的共軛複數，避免重複輸出

    for r in unique_roots:
        count = root_counts[r] # 重根次數
        
        # --- 情況 A: 實數根 ---
        if isinstance(r, float) or r.imag == 0:
            real_val = r.real
            # 針對重根次數 k = 0 到 m-1
            for k in range(count):
                term_str = f"C_{C_index}"
                
                # 處理 x 的冪次 (重根產生 x)
                if k == 1:
                    term_str += "x"
                elif k > 1:
                    term_str += f"x^{k}"
                
                # 處理指數部分 e^(rx)
                if real_val == 0:
                    pass # e^0 = 1，不顯示
                elif real_val == 1:
                    term_str += "e^(x)"
                else:
                    # 去除 .0 以美化輸出 (如 2.0x -> 2x)
                    val_str = f"{real_val:g}" 
                    term_str += f"e^({val_str}x)"
                
                terms.append(term_str)
                C_index += 1

        else:
            
            if r.imag < 0 and r.conjugate() in root_counts:
                continue # 跳過，等待處理它的共軛夥伴 (imag > 0 的那個)
            
            alpha = r.real
            beta = abs(r.imag)
            
            for k in range(count):
                # 複數根一組會產生兩個項：cos 和 sin
                
                # 建構 x 冪次前綴
                x_str = ""
                if k == 1: x_str = "x"
                elif k > 1: x_str = f"x^{k}"
                
                # 建構指數部分 e^(alpha x)
                exp_str = ""
                if alpha != 0:
                    val_str = f"{alpha:g}"
                    if alpha == 1: exp_str = "e^(x)"
                    elif alpha == -1: exp_str = "e^(-x)"
                    else: exp_str = f"e^({val_str}x)"
                
                # 建構三角函數部分 cos(beta x) 和 sin(beta x)
                beta_str = f"{beta:g}"
                if beta == 1:
                    cos_part = f"cos(x)"
                    sin_part = f"sin(x)"
                else:
                    cos_part = f"cos({beta_str}x)"
                    sin_part = f"sin({beta_str}x)"
                
                # 組合 C_n ... cos ...
                term_cos = f"C_{C_index}{x_str}{exp_str}{cos_part}"
                C_index += 1
                
                # 組合 C_n+1 ... sin ...
                term_sin = f"C_{C_index}{x_str}{exp_str}{sin_part}"
                C_index += 1
                
                terms.append(term_cos)
                terms.append(term_sin)

    result = " + ".join(terms)
    return f"y(x) = {result}"

if __name__ == "__main__":
    # 範例測試 (1): 實數單根: y'' - 3y' + 2y = 0  根: 1, 2
    print("--- 實數單根範例 ---")
    coeffs1 = [1, -3, 2]
    print(f"方程係數: {coeffs1}")
    print(solve_ode_general(coeffs1))

    # 範例測試 (2): 實數重根: y'' - 4y' + 4y = 0  根: 2, 2
    print("\n--- 實數重根範例 ---")
    coeffs2 = [1, -4, 4]
    print(f"方程係數: {coeffs2}")
    print(solve_ode_general(coeffs2))

    # 範例測試 (3): 複數共軛根: y'' + 4y = 0  根: 2i, -2i
    print("\n--- 複數共軛根範例 ---")
    coeffs3 = [1, 0, 4]
    print(f"方程係數: {coeffs3}")
    print(solve_ode_general(coeffs3))

    # 範例測試 (4): 複數重根 (二重): (D^2 + 1)^2 y = 0  根: i, i, -i, -i
    print("\n--- 複數重根範例 ---")
    coeffs4 = [1, 0, 2, 0, 1]
    print(f"方程係數: {coeffs4}")
    print(solve_ode_general(coeffs4))

    # 範例測試 (5): 高階重根: y''' - 6y'' + 12y' - 8y = 0  根: 2, 2, 2
    print("\n--- 高階重根範例 ---")
    coeffs5 = [1, -6, 12, -8]
    print(f"方程係數: {coeffs5}")
    print(solve_ode_general(coeffs5))
