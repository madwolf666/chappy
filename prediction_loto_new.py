import pandas as pd
import matplotlib.pyplot as plt

from sklearn import model_selection
from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor

import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

from pandas import datetime
import numpy as np

import itertools
import math

def _read_loto_result():
    _df_loto = pd.read_csv('C:\\Users\\hal\\Downloads\\loto6.csv', sep=",", encoding='shift_jis')
    #print(_df_loto)
    x_train, x_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.2)
    return
    for a_i in range(1, 2):
        a_num_str = '第' + str(a_i) + '数字'
        # 過去の当選結果の抽出
        _df_loto_sub = _df_loto[['日付', a_num_str]]
        print(_df_loto_sub)
        #plt.plot(_df_loto_sub)
        #plt.show()

        ########################################
        # 欠損データの削除
        ########################################
        #_df_loto_sub = _df_loto_sub.dropna()

        ########################################
        # One-hotエンコーディング
        ########################################

        ########################################
        # 学習
        ########################################
        X = _df_loto_sub['日付']
        Y = _df_loto_sub[a_num_str]
        x_train, x_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.2)
        # 正規化
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

        ########################################
        # Keras読込
        ########################################
        # モデルの取得
        model = KerasRegressor(build_fn=reg_model, epochs=200, batch_size=16, verbose=0)
        # 学習
        model.fit(x_train, y_train)

        # スコア（参考値）
        model.score(x_test, y_test)

        ########################################
        # 検証
        ########################################

        ########################################
        # 予測
        ########################################

# モデル生成用関数
def reg_model():
    reg = Sequential()

    reg.add(Dense(10, input_dim=len(2), activation='relu'))
    reg.add(Dense(16, activation='relu'))
    reg.add(Dense(1))
    reg.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    reg.summary()

    return reg

def _predict_Loto(h_num, h_s, h_pred_date_start, h_pred_date_end):
    ########################################
    # データの読み込みと整理⇒ヘッダは読み込まれない
    ########################################
    a_data_csv = pd.read_csv('C:\\Users\\hal\\Downloads\\loto' + str(h_num) + '.csv', sep=",", encoding='shift_jis', dtype=None)

    # 日付の最初と最後を取得（日付は2列目）
    a_date_first = a_data_csv.iat[0, 1].replace("/", "-")
    a_date_last = a_data_csv.iat[len(a_data_csv) - 1, 1].replace("/", "-")

    # 日付のインデックスを作成
    a_index = pd.date_range(a_date_first, a_date_last, dtype='datetime64[ns]', freq="D")
    #print(len(a_index.values))

    # 日付のインデックスでループし、CSVデータの空き行を調整する
    if (h_num == 6):
        a_df_csv = pd.DataFrame(columns=['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', 'BONUS数字', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', 'キャリーオーバー'])
    elif(h_num == 7):
        a_df_csv = pd.DataFrame(columns=['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', '第7数字', 'BONUS数字1', 'BONUS数字2', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '6等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', '6等賞金', 'キャリーオーバー'])

    a_row_c = 0
    for a_row_i in range(0, len(a_index.values)):
        #print('index = ' + str(a_row_i))
        #print('csv = ' + str(a_row_c))
        a_val_i = str(a_index[a_row_i])[:10]
        a_date_i = datetime.strptime(a_val_i, '%Y-%m-%d')
        #print(a_date_i)

        a_val_c = str(a_data_csv.iat[a_row_c, 1])
        a_date_c = datetime.strptime(a_val_c, '%Y/%m/%d')
        #print(a_date_c)
        if (a_date_c == a_date_i):
            # 日付が同じの場合、インデックスの値を再設定
            a_df_csv = a_df_csv.append(a_data_csv.iloc[a_row_c])
            #print('同じ ' + str(a_row_c))
            # CSVデータ参照を1インクリメント
            a_row_c += 1
        else:
            # 日付が異なる場合、インデックスの値を挿入
            if (h_num == 6):
                a_df_csv_c = pd.DataFrame([[0, a_val_i, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], columns=['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', 'BONUS数字', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', 'キャリーオーバー'])
            elif(h_num == 7):
                a_df_csv_c = pd.DataFrame([[0, a_val_i, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], columns=['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', '第7数字', 'BONUS数字1', 'BONUS数字2', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '6等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', '6等賞金', 'キャリーオーバー'])
            #a_df_csv_c = pd.DataFrame([[0, a_val_i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], columns=['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', 'BONUS数字', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', 'キャリーオーバー'])
            a_df_csv = a_df_csv.append(a_df_csv_c)
            #print('異なる ' + str(a_row_c))

    #print(a_df_csv)
    # インデックスを設定
    a_df_csv.index = a_index
    # 日付の列を削除
    del a_df_csv['日付']
    print(a_df_csv)

    ########################################
    # 第x数字毎に予測
    ########################################
    a_pred_num = []
    #h_num = 1
    for a_i in range(1, h_num + 1):
        a_num_str = '第' + str(a_i) + '数字'
        a_df = a_df_csv[[a_num_str]]

        ########################################
        # Dickey-Fuller test（定常性をチェック）
        ########################################

        ########################################
        # 対数をとって傾向を確認
        ########################################
        a_df_log = _get_RatingLog(a_df)

        ########################################
        # 対数データについて、傾向、季節性、残差を眺めてみる
        ########################################
        a_trend_max, a_seasonal_max, a_residual_max = _check_Decompose(a_num_str, a_df_log)

        ########################################
        # SARIMAモデルの最適なパラメータを探す
        ########################################
        # 356 * 2 日周期にしてみる
        a_period = 356*2
        a_period = h_s  #7
        #a_df_period = a_df.iloc[:a_period]
        a_df_period = a_df

        a_ret_params_SARIMA = _select_parameter_SARIMA(a_df_period, a_trend_max, a_seasonal_max, a_residual_max, a_period)
        print(a_ret_params_SARIMA)
        #break

        ########################################
        # モデルの当てはめ
        ########################################
        # order（p：自己相関度, d：誘導, q：移動平均）
        # seasonal_order（p：自己相関度, d：誘導, q：移動平均, s：周期）
        a_SARIMA = sm.tsa.statespace.SARIMAX(a_df, order=a_ret_params_SARIMA[0], seasonal_order=a_ret_params_SARIMA[1]).fit()
        # 結果を確認
        print(a_SARIMA.summary())

        # 残差・自己相関・偏自己相関のチェック
        _cehck_Residual(a_SARIMA, a_period)

        # predに予測データを代入する
        a_pred = a_SARIMA.predict(h_pred_date_start, h_pred_date_end)
        print(a_pred)
        a_pred_num.append(a_pred[len(a_pred) - 1])

        # preadデータともとの時系列データの可視化
        '''
        plt.plot.__init__()
        plt.title("No." + str(str(a_i)))
        plt.xlabel("date")
        plt.ylabel("number")
        plt.plot(a_df)
        plt.plot(a_pred,color="r")
        plt.show()
        '''

    return a_pred_num

# 対数をとって傾向を確認
def _get_RatingLog(h_df):
    a_df_log = np.log(h_df)
    return a_df_log

    plt.plot(a_df_log, label='rating(log)')
    plt.title('rating time series data')
    plt.legend(loc='best')
    plt.show()

    return a_df_log

# 対数データについて、傾向、季節性、残差を眺めてみる
def _check_Decompose(h_num_str, h_df_log):
    # 傾向(trend)、季節性(seasonal)、残差(residual)に分解してモデル化する。
    a_decomposition = seasonal_decompose(h_df_log)
    a_trend = a_decomposition.trend
    a_seasonal = a_decomposition.seasonal
    a_residual = a_decomposition.resid

    #print(a_trend[a_trend[h_num_str] == a_trend[h_num_str]])
    # Nanを除外
    a_val = max(a_trend[h_num_str][a_trend[h_num_str] == a_trend[h_num_str]])
    a_trend_max = math.ceil(a_val)
    print(a_trend_max)
    a_val = max(a_seasonal[h_num_str][a_seasonal[h_num_str] == a_seasonal[h_num_str]])
    a_seasonal_max = math.ceil(a_val)
    print(a_seasonal_max)
    a_val = max(a_residual[h_num_str][a_residual[h_num_str] == a_residual[h_num_str]])
    a_residual_max = math.ceil(a_val)
    print(a_residual_max)

    return a_trend_max, a_seasonal_max, a_residual_max

    # オリジナルの時系列データプロット
    plt.subplot(411)
    plt.plot(h_df_log, label='Original')
    plt.legend(loc='best')

    # trend のプロット
    plt.subplot(412)
    plt.plot(a_trend, label='Trend')
    plt.legend(loc='best')

    # seasonal のプロット
    plt.subplot(413)
    plt.plot(a_seasonal,label='Seasonality')
    plt.legend(loc='best')

    # residual のプロット
    plt.subplot(414)
    plt.plot(a_residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.show()

    return a_trend_max, a_seasonal_max, a_residual_max

# SARIMAモデルの最適なパラメータを探す
def _select_parameter_SARIMA(DATA, max_p, max_d, max_q, s):
    p = range(0, max_p + 1)
    d = range(0, max_d + 1)
    q = range(0, max_q + 1)
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
                if (results.bic == results.bic):
                    # nanの場合はアペンドしない
                    parameters.append([param, param_seasonal, results.bic])
                    BICs = np.append(BICs,results.bic)
            except:
                continue
    #print(parameters)
    #print(parameters[0][2])
    return parameters[np.argmin(BICs)]

# 残差・自己相関・偏自己相関のチェック
def _cehck_Residual(h_SARIMA, h_period):
    # 残差のチェック
    a_resid_SARIMA = h_SARIMA.resid
    return

    a_fig = plt.figure(figsize=(12, 8))

    # 自己相関
    a_ax1 = a_fig.add_subplot(211)
    a_fig = sm.graphics.tsa.plot_acf(a_resid_SARIMA, lags=h_period, ax=a_ax1)

    # 偏自己相関⇒★エラーとなる
    a_ax2 = a_fig.add_subplot(212)
    a_fig = sm.graphics.tsa.plot_pacf(a_resid_SARIMA, lags=h_period, ax=a_ax2)

if __name__ == '__main__':
    #Loto6
    a_pred_num = _predict_Loto(6, 14, '2017-12-01', '2018-1-18')
    print('### Loto' + str(6) + ' 予想 ###\n')
    print(a_pred_num)

    #Loto7
    #a_pred_num = _predict_Loto(7, 7, '2017-12-01', '2018-1-19')
    #print('### Loto' + str(7) + ' 予想 ###\n')
    #print(a_pred_num)
