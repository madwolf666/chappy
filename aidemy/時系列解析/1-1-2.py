# 時系列データの表し方

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
# データの読み込み(StatsModelsのテストデータを用います)
co2_tsdata = sm.datasets.co2.load_pandas().data
# 欠損値の処理
co2_tsdata2 = co2_tsdata.fillna(method="ffill")

# x軸の期間を1995年から2000年までに、y軸は値を355から375までに指定したうえでデータを折れ線グラフで表してください
# グラフのタイトルを定める
plt.title("Mauna Loa Weekly Atmospheric CO2 Data")
# グラフのx軸とy軸の名前設定
plt.xlabel("date")
plt.ylabel("CO2 Concentration ppmv")
# ここに答えを記入してください
plt.plot(co2_tsdata2)
plt.xlim("1995", "2000")
plt.ylim(355, 375)

plt.show()
