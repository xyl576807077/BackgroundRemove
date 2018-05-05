res = {}
with open('./generate_word.txt', 'r') as f:
    for line in f.readlines():
        for word in line:
            res[word] = res.get(word, 0) + 1
print(res)