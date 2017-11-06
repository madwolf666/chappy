import sys
import logging
import shutil, os
import csv
import imghdr
from distutils import dir_util
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

def Store_DataFile(h_fileName):
    a_textLine = []
    #a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='shift_jis'))
    a_csv_obj = csv.reader(open(h_fileName, 'r', encoding='utf-8'))
    for v in a_csv_obj:
        a_textLine.append(v)

    return a_textLine

def _checkFile(h_path):
    a_files = os.listdir(h_path)
    for a_file in a_files:
        a_fname = h_path + "\\" + a_file
        if os.path.isfile(a_fname) == True:
            a_imagetype = imghdr.what(a_fname)
            if (a_imagetype == 'jpeg'):
                logging.info('画像ファイル：%s', a_fname)
                exif_data = get_exif_of_image(a_fname)
                if (len(exif_data) > 0):
                    for key, value in exif_data.items():
                        #print(key, value)
                        if (key == 'GPSInfo'):
                            for key2, value2 in value.items():
                                #print(key2, value2)
                                if (key2 == 'GPSLatitude'):
                                    print(get_10_from_60_exif('GPSLatitudeRef', value2))
                                if (key2 == 'GPSLongitude'):
                                    print(get_10_from_60_exif('GPSLongitudeRef', value2))

        if os.path.isdir(a_fname) == True:
            _checkFile(h_path + "\\" + a_file)

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

if __name__ == '__main__':
    #_checkFile("C:\\Users\\hal\\Documents\\tmp\\tmp")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    a_args = sys.argv
    logging.info('GPS画像指定ファイル：%s', a_args[1])
    backup_tree = Store_DataFile(a_args[1])

    for a_tree in backup_tree:
        logging.info('解析元：%s', a_tree[0])

        _checkFile(a_tree[0])
