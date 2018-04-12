import os
from PIL import Image

def png_to_jpg(path):
    files = os.listdir(path)
    for file in files:
        rel = os.path.join(path, file)
        basename = os.path.splitext(rel)[0]
        new_image_path = basename + '.jpg'
        print(new_image_path)
        img = Image.open(rel)
        rgb_im = img.convert('RGB')
        rgb_im.save(new_image_path)
        os.remove(rel)

png_to_jpg('./img/data')