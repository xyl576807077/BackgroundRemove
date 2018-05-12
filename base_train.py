import pickle
import json
from collections import OrderedDict
from util import *
from char_process import CharProcess
import numpy as np

cp = CharProcess()

generate_path = 'generate_from_train1.txt'
with open('./data/train_word_list1.json', 'r') as f:
	word_list = json.load(f)

with open(generate_path, 'w') as f:
	for key, value in word_list.items():
		value = value.strip()
		f.write(value + '\n')

res = [[], [], [], []]
All = []
length_ratio = {}
_sum = 0
for key, value in word_list.items():
	length = len(value) if len(value) <= 20 else 20
	if len(value) > 20:
		value = value[:20]
	code = hard_encode_language(value)
	res[code].append(value)


	All.append(value)
	length_ratio[length] = length_ratio.get(length, 0) + 1
	_sum += 1


language_ratio = {}
extra = 0
for i in range(4):
	language_ratio[i] = int((1000000 - _sum) * len(res[i]) / _sum)
	extra += language_ratio[i]



language_and_length_dict = init_language_and_length(All)

while extra != 0:
	language = random_interval_select(language_ratio)
	length = random_interval_select(length_ratio)
	index = int(np.random.uniform(0, len(All)))
	sen = All[index]
	if len(sen) > length:
		new_sen = cut_sentence(sen, length)
		new_sen = remove_other_language(new_sen, language)
		if new_sen == '':
			continue
		
		if hard_encode_language(new_sen) != language:
			tmp_code = hard_encode_language(new_sen)
			difference_length = length - len(new_sen)
			if difference_length == 0:
				difference_length = 1
			select_code = tmp_code
			while select_code == tmp_code:
				select_code = int(np.random.uniform(0, 4))
			
			
			if language_and_length_dict[select_code].get(difference_length) == None:
				keys = list(language_and_length_dict[select_code].keys())
				index = int(np.random.uniform(0, len(keys)))
				difference_length = keys[index]
			
			canditate = language_and_length_dict[select_code][difference_length]
			select_index = int(np.random.uniform(0, len(canditate)))
			tmp_sen = canditate[select_index]      
			new_sen += tmp_sen
			assert hard_encode_language(new_sen) == language
		
		else:
			difference_length = length - len(new_sen)
			if difference_length == 0:
				continue

			if language_and_length_dict[language].get(difference_length) == None:
				keys = list(language_and_length_dict[language].keys())
				index = int(np.random.uniform(0, len(keys)))
				difference_length = keys[index]
			
			canditate = language_and_length_dict[language][difference_length]
			select_index = int(np.random.uniform(0, len(canditate)))
			tmp_sen = canditate[select_index]
			new_sen += tmp_sen
		
		with open(generate_path, 'a') as f:
			f.write(new_sen + '\n')
		extra -= 1
		print(extra)
		language_ratio[language] -= 1


		
		
