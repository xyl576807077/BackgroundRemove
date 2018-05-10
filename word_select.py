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
    def __init__(self, label_path, frequency):
        with open(label_path, 'r') as f:
            _ = json.load(f)
            labels = list(_.keys())
            labels.remove('\ue76c')
            labels.remove('$$')
        
        self.language_ratio = {}
        for label in labels:
            index = hard_encode(label)
            self.language_ratio[index] = self.language_ratio.get(index, 0) + 1
        
        self.freq = [{}, {}, {}, {}]
        
        tmp = classify(labels)
        for i in range(len(tmp)):
            words = tmp[i]
            for w in words:
                self.freq[i][w] = frequency
        
        

        self.len_ratio = {1: 22963, 2: 21997, 3: 73336, 4: 25366, 
                          5: 12318, 6: 9778,  7: 7699,  8: 6191,
                          9: 4090,  10: 3356, 11: 2763, 12: 1841,
                          13: 1429, 14: 1052, 15: 900,  16: 700,
                          17: 593,  18: 454,  19: 405,  20: 295,
                          21: 2492}
    
    
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

    def get_word_language(self):
        length = self.get_seq_len()
        res = {}
        for i in range(length):
            label = random_interval_select(self.language_ratio)
            res[label] = res.get(label, 0) + 1
        return res


    def get_words(self, func=[]):
        lang_word_dic = self.get_word_language()
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

        for key, value in lang_word_dic.items():
            for j in range(value):
                w = random_interval_select(self.freq[key])
                self.update_freq([w])
                words += w
        return words


    # def __init__(self, label_path, frequency_path):
    #     with open(label_path, 'r', encoding='utf-8') as f:
    #         self.label = list(json.load(f).keys())
    #         self.label.remove('\ue76c')
    #         self.label.remove('$$')
        
    #     with open(frequency_path, 'r', encoding='utf-8') as f:
    #         self.frequency = json.load(f)
    #         for item in self.label:
    #             if self.frequency.get(item, -1) == -1:
    #                 self.frequency[item] = 0
    #         self.classify()
    
    # def __call__(self, length, language, **args):
        
    #     if language == "chinese":
    #         labels = self.pipeline(self.simplifiedchinese, function=args["function"])
    #     elif language == "english":
    #         labels = self.pipeline(self.english, function=args["function"])
    #     elif language == "symbol":
    #         labels = self.pipeline(self.symbol, function=args["function"])
    #     else:
    #         raise NameError("please specify language: chinese, english and symbol")

    #     return labels
    
    
    # def classify(self):
    #     self.simplifiedchinese = []
    #     self.traditionalchinese = []
    #     self.english = []
    #     self.symbol = []
    #     cp = CharProcess()
    #     for item in self.label:
    #         if cp.ishan(item):
    #             t = Converter('zh-hans').convert(item)
    #             if t == item:
    #                 self.simplifiedchinese.append(item)
    #             else:
    #                 self.traditionalchinese.append(item)
    #         elif cp.is_pure_char(item):
    #             self.english.append(item)
    #         else:
    #             self.symbol.append(item)
    
    # # function = [func1, func2]
    # def pipeline(self, labels, **args):
    #     function = args["function"]
    #     for func in function:
    #         labels = func(labels)
    #     return labels
        
    



# wordselect = WordSelect('./data/all_chars_dict.json', 2570)
# print(wordselect.freq)
# i = 1
# while(1):
#     print(i)
#     i += 1
#     words = wordselect.get_words(func=[only_full, only_half])
#     if words == None:
#         break
#     with open('./generate_word.txt', 'a') as f:
#         f.write(words + '\n')
    # with open('./log.txt', 'a') as f:
    #     tmp = ''
    #     for key, value in wordselect.language_ratio.items():
    #         tmp = tmp + str(key) + ':' + str(value) + '\t'
    #     tmp += '\n'
    #     f.write(tmp)