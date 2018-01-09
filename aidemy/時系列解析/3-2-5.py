# 季節調整の利用

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime
import statsmodels.api as sm
import numpy as np
# データの読み込み
co2_tsdata = sm.datasets.co2.load_pandas().data
# 欠損値の処理
co2_tsdata2 = co2_tsdata.dropna()
# 季節調整とグラフのプロット
res = sm.tsa.seasonal_decompose(co2_tsdata2,freq=51)
fig = res.plot()
plt.show()
# 何も書き込まず実行してください
