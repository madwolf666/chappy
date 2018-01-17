# axis

import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 12], [15, 20, 22]])

# arrの行の合計値を求め、問題文の1次元配列を返してください。
# 列：axis=0
# 行：axis=1
print(arr.sum(axis=1))

