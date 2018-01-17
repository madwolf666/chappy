# DataFrameの行間または列間の差を求める

import numpy as np
import pandas as pd
np.random.seed(0)
columns = ["apple", "orange", "banana", "strawberry", "kiwifruit"]

# DataFrameを生成し、列を追加
df = pd.DataFrame()
for column in columns:
    df[column] = np.random.choice(range(1, 11), 10)
df.index = range(1, 11)

# dfの各行について、2行後の行との差を計算したDataFrameをdf_diffに代入してください
# df.diff("行または列の間隔", axis="方向")と指定することで行間または列間の差を計算したDataFrameが作成されます
df_diff = df.diff(-2, axis=0)

# dfとdf_diffの中身を比較して処理内容を確認してください
print(df)
print(df_diff)
