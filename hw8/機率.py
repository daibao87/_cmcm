import math

def calculate_coin_prob():
    p = 0.5
    n = 10000

    print("--- 1. 直接計算 p^n ---")
    try:
        # 這通常會因為數值過小變成 0.0
        direct_prob = p ** n
        print(f"直接計算 0.5^10000 = {direct_prob}")
    except Exception as e:
        print(f"計算錯誤: {e}")

    print("\n--- 2. 使用 Log 計算 log(p^n) ---")
    # log(p^n) = n * log(p)
    # 我們使用 log10 以便直觀理解數量級 (10的幾次方)
    log_val = n * math.log10(p)
    
    print(f"log10(0.5^10000) = {log_val:.4f}")
    print(f"這代表機率約為: 10 的 {log_val:.4f} 次方")
    print("(這是一個極小極小的數字，前面有約 3010 個零)")

calculate_coin_prob()
