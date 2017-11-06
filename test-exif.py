from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS


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
    exif_data = get_exif_of_image(u"C:\\Users\\hal\\Documents\\tmp\\AkihabaraKousaten.jpg")
    for key, value in exif_data.items():
        #print(key, value)
        if (key == 'GPSInfo'):
            for key2, value2 in value.items():
                #print(key2, value2)
                if (key2 == 'GPSLatitude'):
                    print(get_10_from_60_exif('GPSLatitudeRef', value2))
                if (key2 == 'GPSLongitude'):
                    print(get_10_from_60_exif('GPSLongitudeRef', value2))

    # => Exif 情報を格納した辞書
    #    Exif 情報がない場合には空の辞書
