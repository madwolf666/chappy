# ブロードキャスト

import numpy as np

# 0から14の整数値をもつ3×5のNumpy配列xを生成
x = np.arange(15).reshape(3, 5)
print(x)

# 0から4の整数値をもつ1×5のNumpy配列yを生成
y = np.array([np.arange(5)])
print(y)

# xのn番目の列のすべての行からnだけ引いてください
z = x - y

# xを出力
print(z)
