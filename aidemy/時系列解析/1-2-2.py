# 対数系列

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# データの読み込み(StatsModelsのテストデータを用います)
macrodata = sm.datasets.macrodata.load_pandas().data
macrodata.index = pd.Index(sm.tsa.datetools.dates_from_range("1959q1","2009q3"))

# アメリカの実質GDPの対数変換前の値を表示します。
print(macrodata.realgdp.head())

# 先程の原型列を対数変換して対数系列にします
# ここに解答を記入してください。
macrodata_realgdp_log = np.log(macrodata.realgdp)

# 対数変換後の値を表示します。
print(macrodata_realgdp_log.head())
