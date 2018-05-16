import json
import os
import re

import numpy as np
from sklearn.cluster import KMeans
from torchvision import transforms

from PIL import Image, ImageDraw, ImageFont, features
from util import *

# class GeneratorImage:

#     def __init__(self, background_path, word_file_path, font_path):
#         self.background_files = os.listdir(background_path)

#         for i in range(len(self.background_files)):
#             self.background_files[i] = os.path.join(background_path, self.background_files[i])

#         with open(word_file_path, 'r') as f:
#                 self.word_dict = json.load(f)
#         self.words = list(self.word_dict.keys())
#         self.rotation_transform = transforms.RandomRotation((-30, 30), resample=Image.BICUBIC)
#         self.random_crop = transforms.RandomCrop(32)
#         self.font_path = font_path

#     def set_font_size(self, size):
#         font = ImageFont.truetype(self.font_path, size)
#         return font

#     def random_get_background(self):
#         background_index = np.random.randint(low=0, high=len(self.background_files))
#         background_file = self.background_files[background_index]
#         background_image = Image.open(background_file)
#         background_image = self.random_crop.__call__(background_image)
#         return background_image

#     def draw_char(self, ch, font, canvas_size):
#         colors = ['#DC143C', '#8B008B', '#E6E6FA', '#1E90FF', '#2F4F4F', '#556B2F', '#8B4513', '#000000']
#         img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
#         draw = ImageDraw.Draw(img)
#         color_index = np.random.randint(0, len(colors))
#         color = colors[color_index]
#         draw.text((0, 0), ch, fill=color, font=font)
#         return img

#     def generator_word_img(self, img):
#         new_img = self.rotation_transform.__call__(img)
#         return new_img

#     def paste(self, word_image, background):
#         h, w = word_image.size
#         r, g, b, a = word_image.split()
#         random_x_offset = np.random.randint(0, 32 - h + 1)
#         random_y_offset = np.random.randint(0, 32 - h + 1)
#         background.paste(word_image, (random_x_offset, random_y_offset,
#                     random_x_offset + h, random_y_offset + w), mask=a)

#         groundtruth = Image.new("L", (32, 32), (0, 0, 0))
#         white_word_img = self.whiten_image(word_image)
#         groundtruth.paste(white_word_img, (random_x_offset, random_y_offset,
#                     random_x_offset + h, random_y_offset + w), mask=a)

#         return background, groundtruth


#     def whiten_image(self, img):
#         r, g, b, a = img.split()
#         r = np.array(r)
#         g = np.array(g)
#         b = np.array(b)
#         r[r != -1] = 255
#         b[b != -1] = 255
#         g[g != -1] = 255
#         r = Image.fromarray(r, 'L')
#         g = Image.fromarray(g, 'L')
#         b = Image.fromarray(b, 'L')
#         new_img = Image.merge("RGBA", (r, g, b, a))
#         return new_img

#     def save_generation_image(self, ch, canvas_size, amount, generation_path,
#                 groundtruth_path, is_need_groundtruth = True):
#         basename = str(self.word_dict[ch])
#         for i in range(amount):

#             random_scale = 0.5 + (1 - 0.5) * np.random.random()
#             from math import ceil
#             size = ceil(canvas_size * random_scale)
#             font = self.set_font_size(size)

#             img = self.draw_char(ch, font, canvas_size)
#             img = self.generator_word_img(img)
#             background = self.random_get_background()
#             mix1, mix2 = self.paste(img, background)

#             generation_save = os.path.join(generation_path, basename + '_%d.jpg' % i)
#             mix1.save(generation_save)

#             if is_need_groundtruth == True:
#                 groundtruth_save = os.path.join(groundtruth_path, basename + '_%d.png' % i)
#                 mix2.save(groundtruth_save)

def random_select_font_size():
	size = int(np.random.uniform(10, 151))
	return size


def draw_character(sentence, font_path, color, angle):
	size = random_select_font_size()
	font = ImageFont.truetype(font_path, size)
	if angle == 0:
		img = Image.new('RGBA', (size * len(sentence), size), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		text_size = draw.textsize(sentence, font=font)
		random_offset = int(np.random.uniform(0, 4))
		img = img.resize((text_size[0] + random_offset, text_size[1]))
		draw = ImageDraw.Draw(img)
		draw.text(center_coordinate(img.size, text_size),
		          sentence, font=font, fill=color, direction='rtl')
	else:
		img = Image.new('RGBA', (size, size * len(sentence)), (0, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		sizelist = []
		h_sum = 0
		max_w = -1
		for i in range(len(sentence)):
			text_size = draw.textsize(sentence[i], font=font)
			# print(text_size)
			sizelist.append(text_size)
			h_sum += text_size[1]
			max_w = max(text_size[0], max_w)
		img = img.resize((max_w, h_sum), Image.BICUBIC)
		draw = ImageDraw.Draw(img)
		h_tmp = 0
		for i in range(len(sentence)):
			w, h = sizelist[i]
			new_coordinate = (w, h)
			block_size = (max_w, h)
			new_coordinate = center_coordinate(block_size, text_size)
			draw.text((new_coordinate[0], new_coordinate[1] + h_tmp), sentence[i], font=font, fill=color)
			h_tmp += h
		img = img.rotate(90, expand=True)
	return img


def center_coordinate(block_size, text_size):
	W, H = block_size
	w, h = text_size
	new_size = ((W-w)/2, (H-h)/2)
	return new_size


def center_edge_coordinate(block_size, text_size, flag):
	W, H = block_size
	w, h = text_size
	if flag == 0:
		new_size = ((W-w)/2, H - h)
	else:
		new_size = ((W-w)/2, 0)
	return new_size


def select_font(sentence, word_font_dict, font_dict):
	font_set = set(word_font_dict[sentence[0]])

	for i in range(1, len(sentence)):
		if sentence[i] == ' ':
			continue
		font_set.intersection_update(word_font_dict[sentence[i]])
		# print(sentence[i], len(font_set))
	font_list = list(font_set)
	assert len(font_set) != 0
	font_name = font_list[int(np.random.uniform(0, len(font_set)))]
	font = font_dict[font_name]

	return font


def random_get_background(background_path):
	files = os.listdir(background_path)
	for i in range(len(files)):
		files[i] = os.path.join(background_path, files[i])
	background_index = int(np.random.uniform(0, len(files)))
	background_file = files[background_index]
	background_image = Image.open(background_file)
	return background_image


def toRgb(hex_color):
	color = hex_color.lstrip('#')
	res = list(int(color[i:i+2], 16) for i in (0, 2, 4))
	return np.array(res)


def random_select_color(img):
	# img = np.array(img)
	# h, w, c = img.shape
	# feature = []
	# for i in range(h):
	#     for j in range(w):
	#         feature.append(img[i][j])

	# clf = KMeans(n_clusters=5, max_iter=10).fit(feature)
	# cluster = clf.cluster_centers_
	basic_color = ['#FF0000', '#FFC0CB', '#FFA500', '#FFFF00',
                '#800080', '#008000', '#0000FF', '#A52A2A', '#FFFFFF', '#808080']

	# pos = -1
	# Min = 1e9
	# for i in range(len(basic_color)):
	#     rgb = toRgb(basic_color[i])
	#     dis = np.sum(np.sqrt(np.multiply(cluster - rgb, cluster - rgb)))
	#     if Min < dis:
	#         Min = dis
	#         pos = i
	# basic_color.pop(pos)

	index = int(np.random.uniform(0, len(basic_color)))
	return basic_color[index]


def paste(word_image, background):
	h, w = word_image.size
	r, g, b, a = word_image.split()

	
	background = background.resize((h, w), Image.BICUBIC)
	background.paste(word_image, (0, 0, h, w), mask=a)

	groundtruth = Image.new('L', (h, w), 0)
	white_word_img = whiten_image(word_image)
	groundtruth.paste(white_word_img, (0, 0, h, w), mask=a)
	return background, groundtruth


def whiten_image(img):
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


if __name__ == '__main__':
	with open('./extra_font1/word_font_dict.json', 'r', encoding='utf-8') as f:
		word_font_dict = json.load(f)

	with open('./extra_font1/font_dict.json', 'r', encoding='utf-8') as f:
		font_dict = json.load(f)

	cnt = 0
	cnt_dict = {}
	rotation_transform = transforms.RandomRotation(
		(-2, 2), resample=Image.BICUBIC, expand=True)
	with open('./5_17_small.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			if len(line) > 20:
				line = line[:20]
			cnt += 1
			code = hard_encode_language(line)
			cnt_dict[code] = cnt_dict.get(code, 0) + 1
			# filename = 'en_' + str(code) + '_' + '%08d' % cnt_dict[code] + '.jpg'
			filename = '%08d' % cnt + '.jpg'
			data_filename = os.path.join('.', 'generate', 'small_data', filename)
			label_filename = os.path.join('.', 'generate','small_label', filename)
			# if os.path.exists(data_filename):
			# 	continue
			background_img = random_get_background('./background')
			color = random_select_color(background_img)
			font = select_font(line, word_font_dict, font_dict)
			word_img = draw_character(line, font, color, 1)
			# try:
			# 	if np.random.uniform(0, 1) > 0.3:
			# 		word_img = draw_character(line, font, color, 0)
			# 	else:
			# 		word_img = draw_character(line, font, color, 1)
			# except:
			# 	continue

			if np.random.uniform(0, 1) < 0.8:
				pass
			else:
				word_img = rotation_transform.__call__(word_img)

			if np.random.uniform(0, 1) < 0.5:
				background_img = random_get_background('./background')
			else:
				background_color = random_select_color(None)
				while background_color != color:
					background_color = random_select_color(None)
				background_img = Image.new('RGB', (64, 64), color=background_color)


			data_img, label_img = paste(word_img, background_img)
			data_img.save(data_filename)
			label_img.save(label_filename)

			print(cnt, font, filename)
			# if cnt > 500:
			# 	break
			# break
