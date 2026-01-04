import random
import matplotlib.pyplot as plt
import math

def estimate_pi_monte_carlo(num_points):
    """
    使用蒙地卡羅方法估算 Pi 值
    :param num_points: 模擬的總點數 (整數)
    :return: 無 (直接顯示圖表與計算結果)
    """
    
    # 初始化計數器與座標列表 (用於繪圖)
    points_inside_circle = 0
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []

    print(f"正在模擬投擲 {num_points} 個點...")

    for _ in range(num_points):
        # 1. 在 [0, 1] 之間隨機生成 x 和 y 座標
        x = random.random()
        y = random.random()

        # 2. 計算點到原點的距離 (判斷是否在單位圓內: x^2 + y^2 <= 1)
        distance = x**2 + y**2

        if distance <= 1:
            points_inside_circle += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)

    # 3. 計算 Pi 的近似值
    # 公式: Pi ~= 4 * (圓內點數 / 總點數)
    pi_estimate = 4 * points_inside_circle / num_points

    # 4. 輸出結果
    print("-" * 30)
    print(f"總點數 (N): {num_points}")
    print(f"圓內點數 (M): {points_inside_circle}")
    print(f"估算的 Pi 值: {pi_estimate}")
    print(f"真實的 Pi 值: {math.pi}")
    print(f"誤差: {abs(pi_estimate - math.pi):.6f}")
    print("-" * 30)

    # 5. 繪製視覺化圖表
    plt.figure(figsize=(6, 6))
    # 畫出圓內的點 (藍色)
    plt.scatter(x_inside, y_inside, color='blue', s=1, label='Inside Circle')
    # 畫出圓外的點 (紅色)
    plt.scatter(x_outside, y_outside, color='red', s=1, label='Outside Circle')
    
    # 設定圖表範圍與標題
    plt.title(f"Monte Carlo Simulation for Pi (N={num_points})\nEstimated Pi = {pi_estimate}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc='upper right')
    plt.axis('equal') # 確保 x, y 軸比例一致，正方形不會變成長方形
    plt.show()

# --- 執行程式 ---
# 建議設定 2000 到 10000 點之間，速度快且效果明顯
estimate_pi_monte_carlo(5000)
