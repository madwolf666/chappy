# 階差をとる

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime
import numpy as np

co2_tsdata = sm.datasets.co2.load_pandas().data
# 欠損値の処理
co2_tsdata2 = co2_tsdata.fillna(method="ffill")
# 原系列のプロット
plt.subplot(2, 1, 1)
plt.xlabel("date")
plt.ylabel("co2")
co2_tsdata2.plot()
# 階差をとる
plt.subplot(2, 1, 2)
plt.xlabel("date")
plt.ylabel("co2_diff")

co2_data_diff = co2_tsdata2.diff()

# 階差系列のプロット
plt.plot(co2_data_diff)
plt.show()
