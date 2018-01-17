# Numpyの高速な処理の体験

# 必要なライブラリをimport
import numpy as np
import time
from numpy.random import rand

# 行、列の大きさ
N = 150

# 行列の初期化
matA = np.array(rand(N, N))
matB = np.array(rand(N, N))
matC = np.array([[0] * N for _ in range(N)])

# Pythonのリストを使って計算

# 開始時間の取得
start = time.time()

# for文を使って行列の掛け算を実行
for i in range(N):
    for j in range(N):
        for k in range(N):
            matC[i][j] = matA[i][k] * matB[k][j]

print("Pythonの機能のみでの計算結果：%.2f[sec]" % float(time.time() - start))

# Numpyを使って計算

# 開始時間の取得
start = time.time()

# Numpyを使って行列の掛け算を実行
matC = np.dot(matA, matB)

# 少数第2位の桁で打ち切っているのでNumpyは0.00[sec]と表示されます。
print("Numpyを使った場合の計算結果：%.2f[sec]" % float(time.time() - start))
