import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms
import numpy as np








# font = ImageFont.truetype('./font/gb2312.ttf', size=32)
# img = draw_char('U', font, 25, 32)
# img.save('./test.png')

class GeneratorImage:

    def __init__(self, background_path, word_file_path):
        self.background_files = os.listdir(background_path)
        for i in range(len(self.background_files)):
            self.background_files[i] = os.path.join(background_path, self.background_files[i])
        self.words = []
        with open(word_file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                self.words.append(line)
        self.rotation_transform = transforms.RandomRotation((-30, 30))
        self.random_crop = transforms.RandomCrop(32)

    def random_get_background(self):
        background_index = np.random.randint(low=0, high=len(self.background_files))
        background_file = self.background_files[background_index]
        background_image = Image.open(background_file)
        background_image = self.random_crop.__call__(background_image)
        return background_image

    def draw_char(self, ch, font, canvas_size):
        colors = ['#DC143C', '#8B008B', '#E6E6FA', '#1E90FF', '#2F4F4F', '#556B2F', '#8B4513', '#000000']
        img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        color_index = np.random.randint(0, len(colors))
        color = colors[color_index]
        draw.text((0, 0), ch, fill=color, font=font)
        return img

    def generator_word_img(self, img):
        h, w = img.size
        random_scale = 0.5 + (1 - 0.5) * np.random.random()
        from math import ceil
        h = ceil(h * random_scale)
        new_img = img.resize((h, h))
        new_img = self.rotation_transform.__call__(new_img)
        return new_img

    def paste(self, word_image, background):
        h, w = word_image.size
        r, g, b, a = word_image.split()
        random_x_offset = np.random.randint(0, 32 - h + 1)
        random_y_offset = np.random.randint(0, 32 - h + 1)
        background.paste(word_image, (random_x_offset, random_y_offset, 
                    random_x_offset + h, random_y_offset + w), mask=a)
        
        groundtruth = Image.new("RGB", (32, 32), (0, 0, 0))
        white_word_img = self.whiten_image(word_image)
        groundtruth.paste(white_word_img, (random_x_offset, random_y_offset, 
                    random_x_offset + h, random_y_offset + w), mask=a)
        
        return background, groundtruth


    def whiten_image(self, img):
        r, g, b, a = img.split()
        r = np.array(r)
        g = np.array(g)
        b = np.array(b)
        r[r != -1] = 255
        b[b != -1] = 255
        g[g != -1] = 255
        r = Image.fromarray(r, 'L')
        g = Image.fromarray(g, 'L')
        b = Image.fromarray(b, 'L')
        new_img = Image.merge("RGBA", (r, g, b, a))
        return new_img
    
    def save_generation_image(self, ch, font, canvas_size, amount, generation_path, groundtruth_path):
        basename = ch.encode('unicode-escape').decode()
        for i in range(amount):
            img = self.draw_char(ch, font, canvas_size)
            img = self.generator_word_img(img)
            background = self.random_get_background()
            mix1, mix2 = self.paste(img, background)

            generation_save = os.path.join(generation_path, basename + '_%d.png' % i)
            groundtruth_save = os.path.join(groundtruth_path, basename + '_%d.png' % i)
            
            mix1.save(generation_save)
            mix2.save(groundtruth_save)
        
        # print(basename.encode('utf-8').decode('unicode_escape'))

