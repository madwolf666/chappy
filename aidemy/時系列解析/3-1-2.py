# 時間情報をインデックスにする

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime

# データの読み込みと整理
sales_sparkring = pd.read_csv(filepath_or_buffer = "https://aidemyexcontentsdata.blob.core.windows.net/data/5060_tsa/monthly-australian-wine-sales-th-sparkling.csv")


# インデックスデータの作成
index = pd.date_range("1980-01-31", "1995-07-31", freq = "M")

# インデックスデータの代入
sales_sparkring.index = index

# "Month"カラムの削除
# ここに答えを書き込んでください
del sales_sparkring["Month"]
# データの表示
print(sales_sparkring.head())
