
# coding: utf-8

# In[ ]:


import json
from char_process import *
from draw_character import *
from torchvision import transforms
from matplotlib.pyplot import imshow
import numpy as np
cp = CharProcess()
generator = GeneratorImage('./img/background/', './data/generate_label.txt')
word_labels = generator.words


# In[ ]:


canvas_size = 32
font = ImageFont.truetype('./font/simsun.ttf', size=canvas_size)
ch = word_labels[0]
# img = generator.draw_char(ch, font, canvas_size)
# img = generator.generator_word_img(img)
# background = generator.random_get_background()
# mix1, mix2 = generator.paste(img, background)
# img = generator.rotation_transform.__call__(img)
# background = Image.open('./img/background/patch_T1.3BPFFJdXXXXXXXX_!!0-item_pic.jpg.jpg')
# paste(img, background)


# In[ ]:

i = 0
for ch in word_labels:
    generator.save_generation_image(ch, font, canvas_size, 10, './img/data/', './img/label/')
    i += 1
    print(i, len(word_labels))


