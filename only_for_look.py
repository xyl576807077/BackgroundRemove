from char_process import CharProcess
from select_rule import *
import json
import pickle
from collections import OrderedDict
from util import *

with open('./data/train_list.json', 'r') as f:
    train_list = json.load(f)

with open('./data/word_dict.pickle', 'rb') as f:
    word_dict = pickle.load(f)

res = {}
for key, value in word_dict.items():
    for w in value:
        if '銷' in value:
            print(key)
            break

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
