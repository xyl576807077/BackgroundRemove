import copy
import json
import os
import sys

import numpy as np

from char_process import *
from langconv import Converter
from select_rule import *
from util import *


class WordSelect:
    def __init__(self, label_path, frequency_path):
        with open(label_path, 'r') as f:
            _ = json.load(f)
            labels = list(_.keys())
            labels.remove('$$')
        
        self.language_ratio = {}
        for label in labels:
            index = hard_encode(label)
            self.language_ratio[index] = self.language_ratio.get(index, 0) + 1
        
        self.freq = [{}, {}, {}, {}]
        
        with open(frequency_path, 'r') as f:
            tmp_freq = json.load(f)
        tmp = classify(labels)
        
        for i in range(len(tmp)):
            words = tmp[i]
            for w in words:
                self.freq[i][w] = tmp_freq[w]
        
        
        self.language_ratio = {0:1028916, 1:0, 2:0, 3:0}
        self.len_ratio = {1: 22963, 2: 21997, 3: 73336, 4: 25366, 
                          5: 12318, 6: 9778,  7: 7699,  8: 6191,
                          9: 4090,  10: 3356, 11: 2763, 12: 1841,
                          13: 1429, 14: 1052, 15: 900,  16: 700,
                          17: 593,  18: 454,  19: 405,  20: 295,
                          21: 2492}
    
    
    def get_language(self):
        language = random_interval_select(self.language_ratio)
        # self.language_ratio[language] -= 1
        return language

    def update_freq(self, select_words):
        for word in select_words:
            code = hard_encode(word)
            if self.freq[code][word] == 1:
                self.language_ratio[code] -= 1
            self.freq[code][word] = max(self.freq[code][word] - 1, 0)
            
    
    def get_canditate(self):
        res = [[], [], [], []]
        for i in range(4):
            words = self.freq[i]
            
            for key, value in words.items():
                if value != 0:
                    res[i].append(key)
                    
        return res
    
    def get_seq_len(self):
        length = random_interval_select(self.len_ratio)
        return length

    def get_word_language(self, flag=None):
        # 检查能不能组成混合的
        chinese = cal_dict_sum(self.freq[0]) + cal_dict_sum(self.freq[1])
        char = cal_dict_sum(self.freq[2])
        symbol = cal_dict_sum(self.freq[3])

        # if flag == None:
        #     language = self.get_language()
        # else:
        #     if flag <= 1028916:
        #         language = 0
        #     elif flag <= 1028916 + 409527:
        #         language = 2
        #     else:
        #         language = 3
        # assert language != 1
        language = 0
        length = self.get_seq_len()
        # print(language, length)
        while language == 3 and length == 1:
            # print('可能死循环')
            length = self.get_seq_len()
        res = {}
        if language == 0:
            simple = cal_dict_sum(self.freq[0])
            tradition = cal_dict_sum(self.freq[1])
            flag = -1
            if simple > length:
                flag = 0
            elif tradition > length:
                flag = 1
            else:
                if simple > tradition:
                    length = simple
                    flag = 0
                else:
                    length = tradition
                    flag = 1
            
            assert length != 0
            for i in range(length):
                res[flag] = res.get(flag, 0) + 1
            print('***\n')
            
        elif language == 2:
            symbol_num = cal_dict_sum(self.freq[3])
            length = length if length < symbol_num else symbol_num
            for i in range(length):
                res[3] = res.get(3, 0) + 1
        
        elif language == 3:
            combination = ['01', '02', '12', '012']
            if chinese == 0:
                combination = ['12']
            if char == 0:
                combination = ['02']
            if symbol == 0:
                combination = ['01']
            print(chinese, char, symbol,combination)
            assert chinese + char + symbol != 0
            index = int(np.random.uniform(0, len(combination)))
            select = combination[index]
            for num in select:
                if int(num) != 0:
                    res[int(num) + 1] = 1
                else:
                    if cal_dict_sum(self.freq[0]) > 0 and cal_dict_sum(self.freq[1]) > 0:
                        prob = np.random.uniform(0, 1)
                        if prob > 0.5:
                            res[0] = 1
                        else:
                            res[1] = 1
                    elif cal_dict_sum(self.freq[0]) > 0:
                        res[0] = 1
                    else:
                        res[1] = 1
            if length < len(select):
                length = len(select)
            else:
                difference = length - len(select)
                canditate = self.get_canditate()
                tmp = []
                for l in canditate:
                    tmp.extend(l)
                canditate = tmp
                cp = CharProcess()
                for i in range(difference):
                    index = int(np.random.uniform(0, len(canditate)))
                    code = hard_encode(canditate[index])
                    res[code] = res.get(code, 0) + 1
                    canditate.pop(index)

        return res


    def get_words(self, func=[], flag=None):
        lang_word_dic = self.get_word_language(flag)
        canditate = self.get_canditate()

        for f in func:
            canditate = f(lang_word_dic, canditate)
        
        flag = 0
        for i in range(4):
            flag += len(canditate[i])

        if flag == 0:
            return None
        # if len(canditate[3]) == 0:
        #     raise NameError("used all symbols")
        
        words = ''
        # print(lang_word_dic)
        for key, value in lang_word_dic.items():
            for j in range(value):
                w = random_interval_select(self.freq[key])
                self.update_freq([w])
                words += w
                
        tmp_dict = {}
        tmp_dict.update(self.freq[0])
        tmp_dict.update(self.freq[1])
        tmp_dict.update(self.freq[2])
        tmp_dict.update(self.freq[3])
        with open('./tmp-1.json', 'w') as f:
            json.dump(tmp_dict, f, ensure_ascii=False)
        return words

    



# wordselect = WordSelect('./data/all_chars_dict.json', './data/5_16_big.json')
# i = 1
# while(1):
    
#     words = wordselect.get_words(func=[only_full, only_half])
#     i += 1

#     if words == None:
#         break
#     print(i)
#     with open('./5_16_big.txt', 'a') as f:
#         f.write(words + '\n')



    # with open('./log.txt', 'a') as f:
    #     tmp = ''
    #     for key, value in wordselect.language_ratio.items():
    #         tmp = tmp + str(key) + ':' + str(value) + '\t'
    #     tmp += '\n'
    #     f.write(tmp)
