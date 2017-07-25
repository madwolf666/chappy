import os
import mimetypes
from PIL import Image

for foldername, subfolders, filenames in os.walk('C:\\Users\\hal\\Documents'):
    num_photo_files = 0
    num_non_photo_files = 0
    for filename in filenames:
        #print(subfolders)
        #print(foldername)
        mime = mimetypes.guess_type(filename)
        #print(mime)

        if (mime[0] != 'image/jpeg') and (mime[0] != 'image/png'):
            num_non_photo_files += 1
            continue

        im = Image.open(foldername + "\\" + filename)
        width, height = im.size
        #print("{width},{height}".format(width=width, height=height))

        if (width > 500) and (height > 500):
            num_photo_files += 1
        else:
            num_non_photo_files += 1

    if num_photo_files > 0:
        print(foldername)