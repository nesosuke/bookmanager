from pyzbar.pyzbar import decode
from PIL import Image

d = decode(Image.open('barcode.png'))

for item in d:
    e = item.data.decode("utf-8")
    if e[0:2] == '97': # ISBNは97から始まるので．
        print(e)