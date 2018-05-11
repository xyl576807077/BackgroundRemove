from char_process import CharProcess
from select_rule import *
import json
import pickle
from collections import OrderedDict
from util import *

with open('./extra_font/word_font_dict.json', 'r') as f:
    dic = json.load(f)

with open('./extra_font/windows_font_dict.json', 'r') as f:
    dic1 = json.load(f)

with open('./data/all_chars_dict.json', 'r') as f:
    all_chars_dict = json.load(f)

common_chinese = set(['著'])

for key in all_chars_dict.keys():
    if hard_encode(key) == 1 and key not in common_chinese:
        dic[key] = dic1[key]

with open('./extra_font/word_font_dict_unstable.json', 'w') as f:
    json.dump(dic, f, ensure_ascii=False)




# 0 0.4606252232006759
# 1 0.32793296575992753
# 2 0.02846516327401639
# 3 0.18297664776538017

# res = {}
# _sum = 0
# cnt = 0
# cp = CharProcess()
# with open('./generate_from_train.txt', 'r', encoding='utf-8') as f:
#     for line in f.readlines():
#         _sum += 1
#         line = line.strip()
#         for w in line:
#             if cp.is_pure_symbol(w):
#                 cnt += 1
#                 break
# print(cnt, cnt / _sum)
