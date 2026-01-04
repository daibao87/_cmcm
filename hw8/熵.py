import numpy as np

def info_theory_metrics():
    # 為了避免 log(0)，我們加上一個極小值 epsilon
    eps = 1e-15

    def entropy(p):
        """熵 H(p)"""
        return -np.sum(p * np.log2(p + eps))

    def cross_entropy(p, q):
        """交叉熵 H(p, q)"""
        return -np.sum(p * np.log2(q + eps))

    def kl_divergence(p, q):
        """KL 散度 D_KL(p || q) = H(p, q) - H(p)"""
        return np.sum(p * np.log2((p + eps) / (q + eps)))

    def mutual_information(pxy, px, py):
        """
        互資訊 I(X;Y)
        pxy: 聯合機率分佈
        px, py: 邊際機率分佈
        """
        mi = 0
        for i in range(len(px)):
            for j in range(len(py)):
                if pxy[i][j] > 0:
                    mi += pxy[i][j] * np.log2(pxy[i][j] / (px[i] * py[j]))
        return mi

    # --- 驗證資料 ---
    # 定義兩個不同的機率分佈
    p = np.array([0.8, 0.1, 0.1]) # 真實分佈
    q = np.array([0.2, 0.4, 0.4]) # 預測分佈 (很不準)
    
    h_p = entropy(p)          # 也就是 cross_entropy(p, p)
    ce_pq = cross_entropy(p, q)
    kl_pq = kl_divergence(p, q)

    print(f"--- 資訊理論指標計算 ---")
    print(f"分佈 P: {p}")
    print(f"分佈 Q: {q}")
    print(f"1. 熵 H(P) (自我交叉熵): {h_p:.4f} bits")
    print(f"2. 交叉熵 H(P, Q): {ce_pq:.4f} bits")
    print(f"3. KL 散度 D_KL(P||Q): {kl_pq:.4f} bits")
    
    # 互資訊範例 (假設 X, Y 關聯性)
    # 聯合分佈矩陣
    p_xy = np.array([[0.1, 0.1], [0.0, 0.8]]) 
    p_x = np.sum(p_xy, axis=1)
    p_y = np.sum(p_xy, axis=0)
    mi_val = mutual_information(p_xy, p_x, p_y)
    print(f"4. 互資訊 I(X;Y): {mi_val:.4f} bits")

    # --- 驗證 Inequality ---
    print("\n--- 驗證 Cross Entropy 不等式 ---")
    print(f"H(P, P) = {h_p:.4f}")
    print(f"H(P, Q) = {ce_pq:.4f}")
    
    if ce_pq > h_p:
        print("驗證結果: H(P, Q) > H(P, P) 成立 (當 P != Q 時)")
        print("說明: 您的原始假設 (p,p) > (p,q) 數學上是不成立的，正確應該是 Cross Entropy 越小越好，最小為 Entropy。")
    else:
        print("驗證失敗")

info_theory_metrics()
