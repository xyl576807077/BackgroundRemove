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

def legitimate_symbol(lines):
    res = []
    cp = CharProcess()
    _sum = 0
    for line in lines:
        cnt = 0
        cnt2 = 0
        tmp = line
        if cp.is_pure_symbol(tmp):
            res.append(tmp)
        if cp.is_pure_symbol(line[0]):
            tmp = first_not_symbol(tmp)
        for i in range(1, len(tmp)):
            if cp.is_pure_symbol(tmp[i]):
                cnt += 1
            else:
                cnt2 += 1
        #没有符号直接放进list
        if cnt == 0:
            res.append(tmp)
            continue
        
        if cnt - cnt2 >= 2:
            tmp = symbol_last_continue(tmp)
        else:
            tmp = symbol_not_continue(tmp)
        res.append(tmp)
    return res

def first_not_symbol(s):
    cp = CharProcess()
    s = list(s)
    for i in range(1, len(s)):
        if cp.is_pure_symbol(s[i]) == False:
            s[0], s[i] = s[i], s[0]
            break
    s = ''.join(s)
    return s

def symbol_not_continue(s):
    cp = CharProcess()
    s = list(s)
    sa = []
    sb = []
    for i in range(1, len(s)):
        if cp.is_pure_symbol(s[i]):
            sb.append(s[i])
        else:
            sa.append(s[i])
    posa = 0
    posb = 0
    for i in range(1, len(s)):
        # 奇数放符号
        if posb == len(sb):
            s[i] = sa[posa]
            posa += 1
            continue
        if i % 2 == 1:
            s[i] = sb[posb]
            posb += 1
        else:
            s[i] = sa[posa]
            posa += 1
    s = ''.join(s)
    return s

def symbol_last_continue(s):
    cp = CharProcess()
    s = list(s)
    tail = len(s) - 1
    i = 1
    while i < tail:
        if cp.is_pure_symbol(s[i]):
            s[i], s[tail] = s[tail], s[i]
            tail -= 1
        if cp.is_pure_symbol(s[i]) == False:
            i += 1
    s = ''.join(s)
    return s
# only_full({0:1, 2:2}, [[],[],[],[',', '。', ':']])
legitimate_symbol(['臣盖括溺泌竹芦捐践鹭题贰岳撮缇帛镯v緯樂π'])
