# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

################################################################################
# Deep Learning関連
################################################################################
def identity_function(x):
    return x


def step_function(x):
    return np.array(x > 0, dtype=np.int)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    return (1.0 - sigmoid(x)) * sigmoid(x)


def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    grad = np.zeros(x)
    grad[x>=0] = 1
    return grad


def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T

    x = x - np.max(x) # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))


def mean_squared_error(y, t):
    return 0.5 * np.sum((y-t)**2)


def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)

    # 教師データがone-hot-vectorの場合、正解ラベルのインデックスに変換
    if t.size == y.size:
        t = t.argmax(axis=1)

    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t])) / batch_size


def softmax_loss(X, t):
    y = softmax(X)
    return cross_entropy_error(y, t)

################################################################################
# Exif関連
################################################################################
# Exifファイルの読み込み
def get_exif_of_image(h_file):
    """Get EXIF of an image if exists.

    指定した画像のEXIFデータを取り出す関数
    @return exif_table Exif データを格納した辞書
    """
    a_im = Image.open(h_file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        a_exif = a_im._getexif()
        if (a_exif == None):
            return {}
    except AttributeError:
        return {}

    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    a_exif_table = {}
    for a_tag_id, a_value in a_exif.items():
        a_tag = TAGS.get(a_tag_id, a_tag_id)

        #GPSは個別の扱う
        if (a_tag == 'GPSInfo'):
            a_gps_data = {}
            for a_t in a_value:
                a_gps_tag = GPSTAGS.get(a_t, a_t)
                a_gps_data[a_gps_tag] = a_value[a_t]
            a_exif_table[a_tag] = a_gps_data
        else:
            a_exif_table[a_tag] = a_value

    return a_exif_table

# 文字列を数値に変換
def convert_float(h_str):
    a_Ret = 0

    if (len(h_str)>=2):
        if (h_str[0] > 0) and (h_str[1] > 0):
            a_Ret = float(h_str[0])/float(h_str[1])
        else:
            a_Ret = 0
    else:
        a_Ret = float(h_str[0])

    return a_Ret

# 60進数を10進数に変換
def get_10_from_60_exif(h_ref, h_gps):
    a_data = convert_float(h_gps[0]) + (convert_float(h_gps[1])/60) + (convert_float(h_gps[2])/3600)

    if (h_ref == 'S') or (h_ref == 'W'):
        a_data *= -1

    return a_data
