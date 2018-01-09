# 階差系列

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# データの読み込み(StatsModelsのテストデータを用います)
co2_tsdata = sm.datasets.co2.load_pandas().data

# 欠損値の処理
co2_tsdata2 = co2_tsdata.fillna(method="ffill")

# データの階差をとります
co2_tsdata2_diff = co2_tsdata2.diff()


plt.subplot(2,1,1)
plt.title("Mauna Loa Weekly Atmospheric CO2 Data")
plt.xlabel("date")
plt.ylabel("CO2 Concentration ppmv")
plt.plot(co2_tsdata2)

plt.subplot(2,1,2)
plt.title("Mauna Loa Weekly Atmospheric CO2 Data DIFF")
plt.xlabel("date")
plt.ylabel("CO2 Concentration ppmv DIFF")
plt.plot(co2_tsdata2_diff)

plt.subplots_adjust(wspace=0, hspace=1.0)

plt.show()

# 何も書き込まずに実行してください
