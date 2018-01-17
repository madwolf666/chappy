# フィルタリング

import numpy as np
import pandas as pd
np.random.seed(0)
columns = ["apple", "orange", "banana", "strawberry", "kiwifruit"]

# DataFrameを生成し、列を追加
df = pd.DataFrame()
for column in columns:
    df[column] = np.random.choice(range(1, 11), 10)
df.index = range(1, 11)

# フィルタリングを用いて、dfの"apple"列が5以上かつ"kiwifruit"列が5以上の値をもつ行を含むDataFrameをdfに代入してください
df = df.loc[df["apple"] >= 5]
df = df.loc[df["kiwifruit"] >= 5]
#df = df.loc[df["apple"] >= 5][df["kiwifruit"] >= 5]でもOK

print(df)
