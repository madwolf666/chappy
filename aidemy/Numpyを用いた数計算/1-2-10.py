# 乱数

import numpy as np

# randint関数をnp.randomとつけなくてもいいようにimportしてください
from numpy.random import randint

# 変数arr1に各要素が0~10までの整数の行列(5×2)を代入してください
arr1 = randint(0, 11, (5, 2))
print(arr1)

# 変数arr2に0~1までの一様乱数を三つ代入してください
arr2 = np.random.rand(3)
print(arr2)
