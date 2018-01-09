# 自己相関係数・偏自己相関係数とその可視化

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime

# データの読み込みと整理
sales_sparkring = pd.read_csv(filepath_or_buffer = "https://aidemyexcontentsdata.blob.core.windows.net/data/5060_tsa/monthly-australian-wine-sales-th-sparkling.csv")
index = pd.date_range("1980-01-31", "1995-07-31", freq="M")
sales_sparkring.index=index
del sales_sparkring["Month"]
# 自己相関・偏自己相関の可視化
fig=plt.figure(figsize=(12, 8))
# 自己相関係数のグラフを出力します
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(sales_sparkring, lags=30, ax=ax1)
# 偏自己相関係数のグラフを出力します
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(sales_sparkring, lags=30, ax=ax2)
plt.show()
# なにも記入せず実行してください
