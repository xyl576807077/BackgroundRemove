import numpy as np
import json
import os
import queue
class WordPriority:

    def __init__(self, priority, word):
        self.priority = priority
        self.word = word

    def __lt__(self, other):
        return self.priority < other.priority

if __name__ == "__main__":
    
    with open('./data/frequency_from_all.json', 'r') as f:
        freq = json.load(f)
    
    q = queue.PriorityQueue()

    for item in freq.keys():
        num = freq[item]
        q.put(WordPriority(num, item))

    while not q.empty():
        hehe = q.get()
        print(hehe.priority, hehe.word)
