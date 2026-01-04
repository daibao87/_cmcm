import numpy as np
from scipy.linalg import lu, qr, svd

np.random.seed(42)

A = np.array([[4., 2., 1.],
              [1., 5., 2.],
              [1., 2., 4.]])

print("原始矩陣 A:\n", A)
print("-" * 30)

def recursive_det(matrix):
    n = matrix.shape[0]
    if n == 2:
        return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
    
    det_val = 0

    for c in range(n):

        sub_matrix = np.delete(np.delete(matrix, 0, axis=0), c, axis=1)
        sign = (-1) ** c
        det_val += sign * matrix[0, c] * recursive_det(sub_matrix)
    return det_val

calc_det = recursive_det(A)
numpy_det = np.linalg.det(A)
print(f"1. 遞迴計算行列式: {calc_det:.4f}")
print(f"   Numpy 驗證: {numpy_det:.4f}")
print("-" * 30)


P, L, U = lu(A)

det_P = np.linalg.det(P) 
det_L = np.prod(np.diag(L)) # 應為 1
det_U = np.prod(np.diag(U))

lu_det = det_P * det_L * det_U
print(f"2. 透過 LU 分解計算行列式: {lu_det:.4f}")
print(f"   L 矩陣 (下三角):\n{L}")
print(f"   U 矩陣 (上三角):\n{U}")
print("-" * 30)

print("3. 分解還原驗證:")

# LU 驗證
A_recalc_lu = P @ L @ U
print(f"   LU 還原誤差: {np.linalg.norm(A - A_recalc_lu):.2e}")

# 特徵值分解 (Eig)
eigenvalues, eigenvectors = np.linalg.eig(A)
# A = V * Lambda * V^-1
D = np.diag(eigenvalues)
V = eigenvectors
V_inv = np.linalg.inv(V)
A_recalc_eig = V @ D @ V_inv
print(f"   Eig 還原誤差: {np.linalg.norm(A - A_recalc_eig):.2e}")

# SVD 分解
U_svd, S_svd, Vt_svd = np.linalg.svd(A)
# A = U * Sigma * V^T
Sigma = np.zeros_like(A)
np.fill_diagonal(Sigma, S_svd)
A_recalc_svd = U_svd @ Sigma @ Vt_svd
print(f"   SVD 還原誤差: {np.linalg.norm(A - A_recalc_svd):.2e}")
print("-" * 30)

ATA = A.T @ A


eig_vals_ATA, V_calc = np.linalg.eig(ATA)

sorted_indices = np.argsort(eig_vals_ATA)[::-1]
sigma_calc = np.sqrt(eig_vals_ATA[sorted_indices])
V_calc = V_calc[:, sorted_indices]
Vt_calc = V_calc.T

Sigma_inv = np.diag(1 / sigma_calc)
U_calc = A @ V_calc @ Sigma_inv

print("4. 用 Eig 手刻 SVD 結果:")
print(f"   手算奇異值: {sigma_calc}")
print(f"   Numpy SVD 奇異值: {S_svd}")
print(f"   重建矩陣誤差: {np.linalg.norm(A - (U_calc @ np.diag(sigma_calc) @ Vt_calc)):.2e}")
print("-" * 30)

print("5. PCA 實作 (使用 SVD):")
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], dtype=float)
print("   原始數據 X:\n", X)

X_mean = np.mean(X, axis=0)
X_centered = X - X_mean

pc1 = Vt_pca[0]

print(f"   數據中心點: {X_mean}")
print(f"   第一主成分方向: {pc1}")

projected_data = X_centered @ pc1.T
print(f"   降維後的數據 (1D): {projected_data}")
