# 定常性の確認（視覚化）

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from pandas import datetime

#ホワイトノイズの設定
mean = 0
std = 1
num_samples = 1000
samples = np.random.normal(mean, std, size=num_samples)
# ホワイトノイズのプロット
plt.title("Whitenoise")
plt.plot(samples)
plt.show()
# 何も書き込まずに実行してください
