# ソート

import numpy as np

arr = np.array([[8, 4, 2], [3, 5, 1]])
print(arr)

# argsort関数を用いて出力してください
print(arr.argsort())

# np.sort()を用いてソートし出力してください
# np.sort()はソートした配列のコピーを返すもの
print(np.sort(arr))

# sort()を用いて行でソートしてください
arr.sort(1)
print(arr)
