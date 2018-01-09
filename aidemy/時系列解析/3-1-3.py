# 折れ線グラフで表示

import numpy as np
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
del sales_sparkring["Month"]

# データを折れ線グラフで表します
# グラフのタイトルを設定
plt.title("monthly-australian-wine-sales-th-sparkling")
# グラフのx軸とy軸の名前設定
plt.xlabel("date")
plt.ylabel("sales")

# データのプロット
# ここに答えを入力してください
plt.plot(sales_sparkring)
plt.show()
