# 参考URL
# http://pythondatascience.plavox.info/wp-content/uploads/2016/07/wine3.png

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

_loto6 = None
_clf = None
_X = None
_Y = None
_except_quality = None

def _read_learned_data():
    global _loto6, _clf

    _loto6 = pd.read_csv('C:\\Users\\hal\\Downloads\\loto6.csv', sep=",", encoding='shift_jis')
    _loto6.head
    _clf = linear_model.LinearRegression()

def _set_value_1(h_num):
    global _loto6, _X, _Y

    #説明変数に"BONUS数字1"を利用
    _X = _loto6.loc[:, ['日付']].as_matrix()

    #目的変数に"第1数字"を利用
    _Y = _loto6['第' + str(h_num) +'数字'].as_matrix()

def _set_value(h_num):
    global _loto6, _X, _Y, _except_quality

    #説明変数に"BONUS数字1"を利用
    #a_drop_col = ['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', '第7数字', 'BONUS数字2', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '6等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', '6等賞金', 'キャリーオーバー']
    #a_drop_col = ['開催回', '日付', '第1数字', '第2数字', '第3数字', '第4数字', '第5数字', '第6数字', '第7数字', 'BONUS数字1', 'BONUS数字2', '1等口数', '2等口数', '3等口数', '4等口数', '5等口数', '6等口数', '1等賞金', '2等賞金', '3等賞金', '4等賞金', '5等賞金', '6等賞金', 'キャリーオーバー']
    a_drop_col = ['開催回', '日付']
    _except_quality = _loto6.drop(a_drop_col, axis=1)
    #print(_except_quality)
    _X = _except_quality.as_matrix()
    #print(_X[len(_X)-1, 0])
    # X から NaN を含む列を削除する
    #_X.drop(_X.columns[np.isnan(_X).any()], axis=1)

    #目的変数に"第1数字"を利用
    _Y = _loto6['第' + str(h_num) + '数字'].as_matrix()

def _create_prediction_model1():
    global _clf, _X, _Y

    #予測モデルを作成
    _clf.fit(_X, _Y)
    #回帰係数
    print('回帰係数：' + str(_clf.coef_))
    #切片（誤差）
    print('切片（誤差）：' + str(_clf.intercept_))
    #決定係数
    print('決定係数' + str(_clf.score(_X, _Y)))

    #予測は？
    #a_clf.coef_ × [BONUS数字] + a_clf.intercept_
    #a_tmp = _X[len(_X)-1, 0] + 3
    a_tmp = _X[len(_X)-1, 0] + 4
    print('a_tmp：' + str(a_tmp))
    a_val = _clf.coef_*(a_tmp) + _clf.intercept_
    print('予測値：' + str(a_val))

def _create_prediction_model():
    global _clf, _X, _Y, _except_quality

    #予測モデルを作成
    _clf.fit(_X, _Y)
    #回帰係数
    df = pd.DataFrame({"Name": _except_quality.columns,
                        "Coefficients": _clf.coef_})
    #df = pd.DataFrame({"Name": _except_quality.columns,
    #                    "Coefficients": _clf.coef_}).sort_values(by='Coefficients')
    #print(df)
    #print(df.iloc[0,0])
    #print(df.loc[:, '1等口数'])

    #切片（誤差）
    print('切片（誤差）：' + str(_clf.intercept_))

    #決定係数
    #print(_clf.score(_X, _Y))

    #予測は？
    #a_clf.coef_ × [BONUS数字] + a_clf.intercept_
    a_val = 0
    for a_num in range(len(df)):
        #print('a_num：' + str(a_num))
        #print('df.iloc[a_num,0]：' + str(df.iloc[a_num,0]))
        #print('_X[len(_X)-1, a_num]：' + str(_X[len(_X)-1, a_num]))
        a_val += (df.iloc[a_num,0])*(_X[len(_X)-1, a_num])
    a_val += _clf.intercept_

    print('予測値：' + str(a_val))

def _show_chart():
    global  _X, _Y

    #散布図
    plt.scatter(_X, _Y)
    #回帰曲線
    plt.plot(_X, _clf.predict(_X))
    plt.show()

if __name__ == '__main__':
    #過去の当選結果を読み込む
    _read_learned_data()
    # 説明変数に"BONUS数字1"を利用
    #_set_value_1()
    # 説明変数に"第1数字"以外を利用
    for a_num in range(6):
        print('********** 第' + str(a_num + 1) + '数字 **********')
        _set_value_1(a_num + 1)
        #_set_value(a_num + 1)
        #予測モデルを作成
        _create_prediction_model1()
        #_create_prediction_model()

    #散布図
    #_show_chart()
