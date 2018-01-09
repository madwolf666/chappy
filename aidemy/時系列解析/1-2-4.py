# 季節調整済み系列

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from numpy import nan as na
import numpy as np

# データの読み込み(StatsModelsのテストデータを用います)
co2_tsdata = sm.datasets.co2.load_pandas().data
co2_tsdata2 = co2_tsdata.fillna(method="ffill")
# 季節調整を行い原系列をトレンド、季節変動、残差に分けて出力します
# ★エラー！
fig = sm.tsa.seasonal_decompose(co2_tsdata2, freq=51).plot()
plt.show()
# 何も書き込まず実行してください
