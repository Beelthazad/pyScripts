#!/usr/bin/env python3
from PIL.ExifTags import TAGS
from PIL import Image
import sys

img = #"1609060501529.png"

try:
    exifData = {}
    file = Image.open(img)
    info = file._getexif()
    print(info)
    if info:
        for (tag, value) in info.items():
            decoded = TAGS.get(tag, tag)
            exifData[decoded] = value
        gps = exifData['GPSInfo']
        if gps:
            print("[X] " + img + " Datos GPS : " + gps)
except:
    pass
