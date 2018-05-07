from char_process import CharProcess
from select_rule import *
cp = CharProcess()
res = {}
with open('./generate_word.txt', 'r') as f:
    res = []
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        res.append(line)
        # for i in range(1, len(line)):
        #     if cp.is_pure_symbol(line[i-1]) and cp.is_pure_symbol(line[i]):
        #         print(line)
        #         break

res = legitimate_symbol(res)
with open('./finish_word.txt', 'a') as f:
    for line in res:
        f.write(line + '\n')
