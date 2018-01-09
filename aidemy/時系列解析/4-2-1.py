# モデルの構築

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import datetime
import numpy as np

# データの読み込みと整理
sales_sparkring = pd.read_csv(filepath_or_buffer = "https://aidemyexcontentsdata.blob.core.windows.net/data/5060_tsa/monthly-australian-wine-sales-th-sparkling.csv")
index = pd.date_range("1980-01-31", "1995-07-31", freq="M")
sales_sparkring.index=index
del sales_sparkring["Month"]

# モデルの当てはめ
SARIMA_sparkring_sales =  sm.tsa.statespace.SARIMAX(sales_sparkring,order=(0, 0, 0),seasonal_order=(0, 1, 1, 12)).fit()


#構築したSARIMAモデルのBICを出力します
print(SARIMA_sparkring_sales.bic)
