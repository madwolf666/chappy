import codecs
from pprint import pprint
import numpy as np
import matplotlib.pylab as plt

_learned_data1 = np.array([])
_learned_data2 = np.array([])
_learned_data3 = np.array([])
_learned_data4 = np.array([])
_learned_data5 = np.array([])
_learned_data6 = np.array([])
_learned_data7 = np.array([])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def _read_learned_data():
    fin = codecs.open('C:\\Users\\hal\\Downloads\\loto7.csv', 'r', 'shift_jis')
    a_rec = 0
    for a_line in fin:
        a_split= a_line.replace("'", "").split(",")
        a_rec+=1
        #1行目はタイトルの為、読み飛ばす
        if (a_rec >= 2):
            _learned_data1 = np.append(_learned_data1, np.array(a_split[2]))
            _learned_data2 = np.append(_learned_data2, np.array(a_split[3]))
            _learned_data3 = np.append(_learned_data3, np.array(a_split[4]))
            _learned_data4 = np.append(_learned_data4, np.array(a_split[5]))
            _learned_data5 = np.append(_learned_data5, np.array(a_split[6]))
            _learned_data6 = np.append(_learned_data6, np.array(a_split[7]))
            _learned_data7 = np.append(_learned_data7, np.array(a_split[8]))

    print('*** 第1数字の当選結果 ***')
    pprint(_learned_data1)
    print('*** 第2数字の当選結果 ***')
    pprint(_learned_data2)
    print('*** 第3数字の当選結果 ***')
    pprint(_learned_data3)
    print('*** 第4数字の当選結果 ***')
    pprint(_learned_data4)
    print('*** 第5数字の当選結果 ***')
    pprint(_learned_data5)
    print('*** 第6数字の当選結果 ***')
    pprint(_learned_data6)
    print('*** 第7数字の当選結果 ***')
    pprint(_learned_data7)

def _sigmoid(n):
    print('***********************')
    Y = sigmoid(_learned_data1)
    print(Y)
    plt.plot(_learned_data1, Y)
    #plt.ylim(-0.1, 1.1)
    plt.show()

if __name__ == '__main__':
    #過去の当選結果を読み込む
    _read_learned_data()
    #第n数字毎に推移を検証
    _sigmoid(1)
    #第n数字毎に予測を検証
