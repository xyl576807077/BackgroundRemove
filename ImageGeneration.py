import json
from char_process import *
from draw_character import *
from torchvision import transforms
from matplotlib.pyplot import imshow
import numpy as np

cp = CharProcess()
generator = GeneratorImage('./img/background/', './data/big_label.json', './font/simsun.ttf')
word_labels = generator.words
canvas_size = 32
font = ImageFont.truetype('./font/simsun.ttf', size=canvas_size)



with open('./data/frequency_from_all.json', 'r') as f:
    frequency_all = json.load(f)





i = 0
for ch in word_labels:
    if frequency_all.get(ch, 0) < 11:
        generator.save_generation_image(ch, canvas_size, 11 - frequency_all.get(ch, 0), 
                    './img/img_generation', '', is_need_groundtruth=False)
        i += 1
        print(i, len(word_labels))


