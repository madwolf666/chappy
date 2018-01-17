# ndarrayの注意点

import numpy as np

# ndarrayをそのまま別の変数に代入した場合の挙動を見て行きましょう。
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)

arr2 = arr1
arr2[0] = 100

# 別の変数への変更が元の変数にも影響されています。
print(arr1)

# ndarrayをcopy( )を使って別の変数に代入した場合の挙動を見て行きましょう。
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)

arr2 = arr1.copy()
arr2[0] = 100

# 別の変数への変更が元の変数には影響を与えていません。
print(arr1)
