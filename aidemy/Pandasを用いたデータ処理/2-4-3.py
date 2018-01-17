# 要約統計量を得る

import numpy as np
import pandas as pd
np.random.seed(0)
columns = ["apple", "orange", "banana", "strawberry", "kiwifruit"]

# DataFrameを生成し、列を追加
df = pd.DataFrame()
for column in columns:
    df[column] = np.random.choice(range(1, 11), 10)
df.index = range(1, 11)

# dfの要約統計量のうち、"mean", "max", "min"を取り出してdf_desに代入してください
# df.describe()はdfの列ごとの 個数 、 平均値 、 標準偏差 、 最小値 、四分位数 、 最大値 を含むをDataFrame返します
df_des = df.describe().loc[["mean", "max", "min"]]

print(df_des)
