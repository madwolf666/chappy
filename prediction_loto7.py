import codecs
from pprint import pprint
import numpy as np
import matplotlib.pylab as plt
from mct_functions import sigmoid, softmax

_learned_data = [[] for j in range(7)]

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
            for a_num in range(7):
                _learned_data[a_num].append(int(a_split[a_num + 2], 10))

    for a_num in range(7):
        print('*** 第' + str(a_num + 1) + '数字の当選結果 ***')
        print(len(_learned_data[a_num]))
        pprint(_learned_data[a_num])

def _transition():
    plt.figure(figsize=(30, 20))

    for a_num in range(7):
        a_x = np.arange(0, len(_learned_data[a_num]), 1)
        a_idx = 1
        if (a_num > 2) and (a_num < 6):
            a_idx = 2
        else:
            a_idx = 3
        plt.subplot(4, 3, a_num + 1)
        plt.plot(a_x, _learned_data[a_num])
        plt.ylim(1, 37)
        plt.title('No.' + str(a_num + 1))
    plt.show()

if __name__ == '__main__':
    #過去の当選結果を読み込む
    _read_learned_data()
    #第n数字毎に推移を検証
    _transition()
    #第n数字毎に予測を検証

