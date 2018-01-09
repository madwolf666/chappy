# 対数変換を用いる方法

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime
import numpy as np

# データの読み込み
sunspots = sm.datasets.sunspots.load_pandas().data
sunspots.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))
del sunspots["YEAR"]

# 対数変換
sunspots_log = np.log(sunspots)

# 対数変換後のグラフ
plt.title("Sunspots")
plt.xlabel("date")
plt.ylabel("sunspots_log")
plt.plot(sunspots_log)
plt.show()
