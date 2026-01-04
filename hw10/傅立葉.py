import math
import cmath  # 用於處理複數運算 (complex math)

# 1. dft(f) 正轉換
# 對應圖片公式：F(w) = sum( f(x) * e^(-i*w*x) )
def dft(x):
    """
    計算離散傅立葉轉換 (Discrete Fourier Transform)
    輸入 x: 原始數據列表 (時域)
    輸出 X: 頻率數據列表 (頻域)
    """
    N = len(x)
    X = []
    
    for k in range(N):  # 對每一個頻率 k
        sum_val = 0
        for n in range(N):  # 對每一個時間點 n
            # 歐拉公式：e^(-ix) = cos(x) - i*sin(x)
            # 在 DFT 中，角度 theta = 2 * pi * k * n / N
            # 正轉換指數為負： -1j
            theta = 2 * math.pi * k * n / N
            w = cmath.exp(-1j * theta) 
            sum_val += x[n] * w
        X.append(sum_val)
        
    return X

# 2. idft(F) 逆轉換
# 對應圖片公式：f(x) = (1/N) * sum( F(w) * e^(i*w*x) )
# 注意：離散版本的係數通常是 1/N，而不是圖片連續版本的 1/2pi
def idft(X):
    """
    計算離散傅立葉逆轉換 (Inverse Discrete Fourier Transform)
    輸入 X: 頻率數據列表 (頻域)
    輸出 x: 還原後的數據列表 (時域)
    """
    N = len(X)
    x_recon = []
    
    for n in range(N):  # 對每一個時間點 n
        sum_val = 0
        for k in range(N):  # 對每一個頻率 k
            # 逆轉換指數為正： +1j
            theta = 2 * math.pi * k * n / N
            w = cmath.exp(1j * theta)
            sum_val += X[k] * w
        
        # 逆轉換通常需要除以 N 來做正規化
        x_recon.append(sum_val / N)
        
    return x_recon

# 3. 驗證某函數 f 正轉換過去，再逆轉換回來，會是原函數 f
if __name__ == "__main__":
    print("--- 開始驗證 ---")
    
    # 建立一個簡單的測試信號 f (例如：[1, 2, 3, 4])
    original_f = [1.0, 2.0, 1.0, -1.0]
    print(f"原始函數 f(x): {original_f}")

    # 步驟 1: 執行 DFT
    F_omega = dft(original_f)
    print("\nDFT 轉換後的 F(w) (複數):")
    for val in F_omega:
        print(f"{val:.2f}")

    # 步驟 2: 執行 IDFT
    reconstructed_f = idft(F_omega)
    
    print("\nIDFT 逆轉換後的 f(x) (複數形式):")
    # 這裡顯示複數形式，因為浮點數運算會有極小的虛部誤差
    for val in reconstructed_f:
        print(f"{val:.2f}")

    # 步驟 3: 驗證是否相等
    # 取實部 (real part) 來比較，並忽略極小的計算誤差
    is_same = True
    tolerance = 1e-9 # 容許誤差值
    
    reconstructed_real = [val.real for val in reconstructed_f]
    
    for i in range(len(original_f)):
        if abs(original_f[i] - reconstructed_real[i]) > tolerance:
            is_same = False
            break
            
    print("\n--- 驗證結果 ---")
    print(f"逆轉換取實部後: {reconstructed_real}")
    
    if is_same:
        print("✅ 成功驗證：正轉換後再逆轉換，數值與原函數一致。")
    else:
        print("❌ 驗證失敗：數值不一致。")
