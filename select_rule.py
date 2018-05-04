import numpy as np
from char_process import CharProcess
# from word_select import WordSelect

def rand(labels, size):
    length = len(labels)
    index = [np.random.randint(0, length) for _ in range(size)]
    new_data = []
    for item in index:
        new_data.append(labels[item])
    return new_data

def only_full(dic, candidate):
    if 0 in dic.keys() or 1 in dic.keys():
        symbol = candidate[3]
        cp = CharProcess()
        res = []
        for item in symbol:
            if cp.is_half(item) == False:
                res.append(item)
        candidate[3] = res

    return candidate

def only_half(dic, candidate):
    if 0 not in dic.keys() and 1 not in dic.keys():
        symbol = candidate[3]
        cp = CharProcess()
        res = []
        for item in symbol:
            if cp.is_half(item) == True:
                res.append(item)
        candidate[3] = res

    return candidate


# only_full({0:1, 2:2}, [[],[],[],[',', '。', ':']])