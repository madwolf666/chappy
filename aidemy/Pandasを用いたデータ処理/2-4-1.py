# 一部の行を得る

import numpy as np
import pandas as pd
np.random.seed(0)
columns = ["apple", "orange", "banana", "strawberry", "kiwifruit"]

# DataFrameを生成し、列を追加
df = pd.DataFrame()
for column in columns:
    df[column] = np.random.choice(range(1, 11), 10)
df.index = range(1, 11)

# dfの冒頭3行を取得し、df_headに代入してください
df_head = df.head(3)

# dfの末尾3行を取得し、df_tailに代入してください
df_tail = df.tail(3)

# 出力
print(df_head)
print(df_tail)
