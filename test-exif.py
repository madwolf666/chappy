import sys
import logging
import shutil, os
import csv
import imghdr
from distutils import dir_util
from libmct import mct_functions

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
                exif_data = mct_functions.get_exif_of_image(a_fname)
                if (len(exif_data) > 0):
                    #print(exif_data)
                    isGPS = False
                    lat = 0
                    lon = 0
                    dt = ''
                    for key, value in exif_data.items():
                        #print(key, value)
                        if (key == 'GPSInfo'):
                            for key2, value2 in value.items():
                                #print(key2, value2)
                                if (key2 == 'GPSLatitude'):
                                    isGPS = True
                                    lat = mct_functions.get_10_from_60_exif('GPSLatitudeRef', value2)
                                    print(lat)
                                if (key2 == 'GPSLongitude'):
                                    isGPS = True
                                    lon = mct_functions.get_10_from_60_exif('GPSLongitudeRef', value2)
                                    print(lon)
                        if (key == 'DateTimeOriginal'):
                            tmp = value.split(" ")
                            dt = tmp[0].replace(":", "/") + " " + tmp[1]
                            print(dt)

                    if (isGPS == True):
                        shutil.copy2(a_fname, ".\\photo\\" + a_file)
                        _makeKML(dt, lat, lon, a_file)

        if os.path.isdir(a_fname) == True:
            _checkFile(h_path + "\\" + a_file)

def _makeKML(h_dt, h_lat, h_lon, h_photo):
    a_tmp = h_photo.split(".")
    a_sw = open(".\\kml\\" + a_tmp[0] + ".kml", 'w', encoding='utf-8')

    a_sw.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    a_sw.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
    a_sw.write('<Document>\n')
    a_sw.write('    <Style id="My_Style">\n')
    a_sw.write('        <IconStyle>\n')
    a_sw.write('            <Icon>\n')
    a_sw.write('                <href>../img/Maru_24x24.png</href>\n')
    a_sw.write('            </Icon>\n')
    a_sw.write('        </IconStyle>\n')
    a_sw.write('    </Style> \n')
    a_sw.write('    <Placemark>\n')
    a_sw.write('        <name>' + h_dt + '</name>\n')
    a_sw.write('        <description>' + h_photo + '</description>\n')
    a_sw.write('        <styleUrl>#My_Style</styleUrl>\n')
    a_sw.write('        <Point>\n')
    a_sw.write('            <coordinates>\n')
    a_sw.write('                ' + str(h_lon) + "," + str(h_lat) + '\n')
    a_sw.write('            </coordinates>\n')
    a_sw.write('        </Point>\n')
    a_sw.write('    </Placemark>\n')
    a_sw.write('</Document>\n')
    a_sw.write('</kml>\n')

    a_sw.close()

if __name__ == '__main__':
    #_checkFile("C:\\Users\\hal\\Documents\\tmp\\tmp")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    shutil.rmtree(".\\kml")
    shutil.rmtree(".\\photo")
    os.mkdir(".\\kml")
    os.mkdir(".\\photo")

    a_args = sys.argv
    logging.info('GPS画像指定ファイル：%s', a_args[1])
    backup_tree = Store_DataFile(a_args[1])

    for a_tree in backup_tree:
        logging.info('解析元：%s', a_tree[0])

        _checkFile(a_tree[0])
