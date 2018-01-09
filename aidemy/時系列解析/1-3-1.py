# 期待値（平均）

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# データの読み込み(StatsModelsのテストデータを用います)
co2_tsdata = sm.datasets.co2.load_pandas().data
# 欠損値の処理
co2_tsdata2 = co2_tsdata.fillna(method="ffill")
# データの平均値を求める
print(np.mean(co2_tsdata2))

# 何も書き込まずに実行してください
