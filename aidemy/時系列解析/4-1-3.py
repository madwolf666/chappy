# パラメータの決定

import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm

# データの読み込みと整理
sales_sparkring = pd.read_csv(filepath_or_buffer = "https://aidemyexcontentsdata.blob.core.windows.net/data/5060_tsa/monthly-australian-wine-sales-th-sparkling.csv")
index = pd.date_range("1980-01-31","1995-07-31",freq="M")
sales_sparkring.index=index
del sales_sparkring["Month"]

# 1年間分のデータにしています
sales_sparkring = sales_sparkring[:12]

# 関数の定義
def selectparameter(DATA,s):
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], s) for x in list(itertools.product(p, d, q))]
    parameters = []
    BICs = np.array([])
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(DATA,
                                                order=param,
                                                seasonal_order=param_seasonal)
                results = mod.fit()
                parameters.append([param, param_seasonal, results.bic])
                BICs = np.append(BICs,results.bic)
            except:
                continue
    return parameters[np.argmin(BICs)]

# 周期を埋めて最適なパラメーターを求めてください
selectparameter(sales_sparkring,12)
