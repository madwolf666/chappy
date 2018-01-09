# 移動平均を用いる

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime
import numpy as np

co2_tsdata = sm.datasets.co2.load_pandas().data
# 欠損値の処理
co2_tsdata2 = co2_tsdata.fillna(method="ffill")
# 原系列のグラフ
plt.subplot(6, 1, 1)
plt.xlabel("date")
plt.ylabel("co2")
plt.plot(co2_tsdata2)
# 移動平均を求める
co2_moving_avg = co2_tsdata2.rolling(window=51).mean()
# 移動平均のグラフ
plt.subplot(6, 1, 3)
plt.xlabel("date")
plt.ylabel("co2")
plt.plot(co2_moving_avg)
# 原系列-移動平均グラフ
plt.subplot(6, 1, 5)
plt.xlabel("date")
plt.ylabel("co2")
mov_diff_co2_tsdata = co2_tsdata2-co2_moving_avg
plt.plot(mov_diff_co2_tsdata)
plt.show()
# 何も書き込まず実行してください
