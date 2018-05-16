import json
import os
import re

import numpy as np
from sklearn.cluster import KMeans
from torchvision import transforms

from PIL import Image, ImageDraw, ImageFont, features
from util import *

with open('./extra_font/word_font_dict.json', 'r') as f:
	word_font_dict = json.load(f)

cp = CharProcess()
big = set()
for key, value in word_font_dict.items():
	if cp.is_pure_symbol(key):
		for w in value:
			big.add(w)

for key, value in word_font_dict.items():
	if cp.is_pure_symbol(key) and key != ' ':
		small = set()
		for w in value:
			small.add(w)
		big = big.intersection(small)
		print(len(big), key)
print(big)