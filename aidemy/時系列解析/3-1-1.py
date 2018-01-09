# データの読み込みと表示

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime

# データの読み込みと整理
sales_sparkring = pd.read_csv(filepath_or_buffer = "https://aidemyexcontentsdata.blob.core.windows.net/data/5060_tsa/monthly-australian-wine-sales-th-sparkling.csv")

# 先頭5つのデータを表示、.head()を用いてください
print(sales_sparkring.head(5))
# 後尾5つのデータを表示、.tail()を用いてください
print(sales_sparkring.tail(5))
