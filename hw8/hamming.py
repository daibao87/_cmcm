def hamming_74_simulation():
    # 定義生成矩陣 G (4x7)
    # 形式為 [I_4 | P]
    G = np.array([
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ])

    # 定義同位檢查矩陣 H (3x7)
    # 形式為 [P^T | I_3]
    H = np.array([
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ])

    # 1. 編碼 (Encoding)
    original_data = np.array([1, 0, 1, 1]) # 4 bits 訊息
    # codeword = data * G (模 2 運算)
    codeword = np.dot(original_data, G) % 2
    
    print("\n--- 7-4 漢明碼模擬 ---")
    print(f"原始資料 (4 bits): {original_data}")
    print(f"編碼後碼字 (7 bits): {codeword}")

    # 2. 模擬雜訊 (加入錯誤)
    received = codeword.copy()
    error_pos = 2 # 假設第 3 個 bit (index 2) 發生翻轉
    received[error_pos] = (received[error_pos] + 1) % 2
    print(f"接收到的碼字 (有錯誤): {received}")

    # 3. 解碼與更正 (Decoding)
    # 計算 Syndrome (症狀值) s = H * r^T
    syndrome = np.dot(H, received) % 2
    # 將二進位 [s0, s1, s2] 轉為十進位，這在 Hamming 碼中通常對應錯誤位置
    # 注意：這裡的矩陣 H 構造決定了 Syndrome 對應哪一個 column
    
    # 為了方便對應，我們尋找 syndrome 與 H 的哪個 column 匹配
    error_index = -1
    for i in range(7):
        if np.array_equal(H[:, i], syndrome):
            error_index = i
            break
            
    print(f"計算 Syndrome: {syndrome}")
    
    if error_index != -1:
        print(f"偵測到錯誤位置: Index {error_index}")
        # 更正錯誤
        received[error_index] = (received[error_index] + 1) % 2
        print(f"更正後的碼字: {received}")
        
        # 取出前 4 位作為解碼資料 (因為我們用系統碼 [I|P])
        decoded_data = received[:4]
        print(f"解碼資料: {decoded_data}")
        print(f"是否與原始資料一致: {np.array_equal(original_data, decoded_data)}")
    else:
        print("未偵測到錯誤")

hamming_74_simulation()
