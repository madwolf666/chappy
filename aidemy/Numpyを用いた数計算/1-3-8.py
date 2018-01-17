# 数学関数

import numpy as np

arr = np.arange(15).reshape(3, 5)
print(arr)

# 変数arrの列ごとの平均を出力してください
print(arr.mean(axis=0))

# 変数arrの行の合計を出力してください
print(arr.sum(axis=1))

# 変数arrの最小値を出力してください
print(arr.min())

# 変数arrのそれぞれの列の最大値のインデックス番号を出力してください
print(arr.argmax(axis=0))
