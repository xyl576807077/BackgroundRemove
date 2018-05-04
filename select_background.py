from PIL import Image, ImageFont
import os
import numpy as np
from torchvision import transforms

class BackgroundSelect:

    def __init__(self, backgound_path):
        self.files = os.listdir(backgound_path)
        for i in range(len(self.files)):
            self.files[i] = os.path.join(backgound_path, self.files[i])
            

    def random_select(self, fixed_width):
        index = np.random.randint(len(self.files))
        img = Image.open(self.files[index])
        rand_crop = transforms.RandomCrop((32, 64))
        
        img = rand_crop.__call__(img)
        img.save('hehe.png')
        img = img.resize((fixed_width, 32), Image.BICUBIC)
        return img

# bg = BackgroundSelect('./img/background')
# img = bg.random_select(144)
# img.show()