import os
from PIL import Image
import numpy as np
from collections import OrderedDict
from langconv import Converter
from char_process import CharProcess

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

def random_interval_select(dic):
    new_dic = OrderedDict()
    cnt = 0
    for key, value in dic.items():
        cnt += value
        if value == 0:
            continue
        new_dic[key] = cnt
    s = np.random.uniform(0, cnt)
    
    for key, value in new_dic.items():
        if s <= value:
            k = key
            break
    try:
        s = k
    except:
        print(s, cnt, dic)
    return k

def simplified_to_tradition(text):
    t = Converter('zh-hant').convert(text)
    return t

def hard_encode(text):
    cp = CharProcess()
    if cp.ishan(text):
        t = Converter('zh-hans').convert(text)
        if t == text:
            return 0
        else:
            return 1
    elif cp.is_pure_char(text):
        return 2
    else:
        return 3

def hard_encode_language(text):
    cp = CharProcess()
    if cp.is_pure_chinese(text):
        return 0
    elif cp.is_pure_char(text):
        return 1
    elif cp.is_pure_symbol(text):
        return 2
    else:
        return 3

def classify(labels):
    res = {}

    for label in labels:
        index = hard_encode(label)
        if res.get(index) == None:
            res[index] = [label]
        else:
            res[index].append(label)
    keys = sorted(list(res.keys()))
    rel_res = [[]] * (max(keys) + 1) 
    for item in keys:
        rel_res[item] = res[item]
    return rel_res

def remove_other_language(text, code):
    if code == 3:
        return text
    else:
        res = ''
        for w in text:
            if hard_encode_language(w) == code:
                res += w
        return res

def cut_sentence(text, length):
    is_first = np.random.uniform(0, 1)
    if is_first > 0.5:
        text = text[0:length]
    else:
        text = text[len(text) - length:]
    assert len(text) == length
    return text

def init_language_and_length(lists):
    res = {0:{}, 1:{}, 2:{}, 3:{}}
    for item in lists:
        code = hard_encode_language(item)
        length = len(item)
        if res.get(code).get(length) == None:
            res[code][length] = [item]
        else:
            res[code][length].append(item)
    return res
# classify(['我', '1', '.'])

# dic = {1: 22963,
#     2: 21997,
#     3: 73336,
#     4: 25366,
#     5: 12318,
#     6: 9778,
#     7: 7699,
#     8: 6191,
#     9: 4090,
#     10: 3356,
#     11: 2763,
#     12: 1841,
#     13: 1429,
#     14: 1052,
#     15: 900,
#     16: 700,
#     17: 593,
#     18: 454,
#     19: 405,
#     20: 295,
#     21: 2492}

# random_interval_select(dic)
# print(hard_encode_language('５Ｖ)'))
# cp = CharProcess()
# text = 'Ｌ、'
# print(cp.is_pure_symbol(text))
# print(cp.is_full_width_symbol('Ｌ'))