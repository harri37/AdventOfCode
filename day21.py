data = """140A
169A
170A
528A
340A"""

# data = """029A
# 980A
# 179A
# 456A
# 379A"""

# data = "1A"

from collections import deque
from copy import deepcopy
import functools
from itertools import permutations

numpad = ["789","456","123","-0A"]
dirpad = ["-^A", "<v>"]

act_dir = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0,1),
    "<": (0,-1)
}

def num_bounds(i, j):
    return 0 <= i < len(numpad) and 0 <= j < 3 and numpad[i][j] != "-"


def dir_bounds(i, j):
    return 0 <= i < len(dirpad) and 0 <= j < 3 and dirpad[i][j] != "-"

def get_neighbours(i, j, in_bounds):
    neighs = []
    for act in act_dir.keys():
        di, dj = act_dir[act]
        if in_bounds(i+di, j+dj):
            neighs.append((act, (i+di, j+dj)))
    return neighs
    
def dir_changes(sequence):
    n = 0
    if sequence == "":
        return 0
    prev = sequence[0]
    i = 1
    while i < len(sequence):
        if sequence[i] != prev:
            n += 1
        prev = sequence[i]
        i += 1
    return n

num_sequences = {}

class Node:
    def __init__(self, pos, prev_node, prev_action):
        self.pos = pos
        self.prev_node = prev_node
        self.prev_action = prev_action
        

for si in range(len(numpad)):
    for sj in range(len(numpad[0])):
        if numpad[si][sj] != "-":
            queue = deque()
            seen = set()
            queue.append(Node((si, sj), None, ""))
            seen.add((si, sj))
            while queue:
                curr = queue.popleft()
                this = deepcopy(curr)
                pos = curr.pos
                seen.add(pos)
                sequence = ""
                while curr:
                    sequence += curr.prev_action
                    curr = curr.prev_node
                sequence = sequence[::-1]
                if dir_changes(sequence) <= 1:
                    if ((si, sj), (pos)) in num_sequences.keys():
                        num_sequences[((si, sj), (pos))].append(sequence + "A")
                    else:
                        num_sequences[((si, sj), (pos))] = [sequence + "A"]            
                neighs = get_neighbours(pos[0], pos[1], num_bounds)
                for act, neigh in neighs:
                    if neigh not in seen:
                        queue.append(Node((neigh[0], neigh[1]), this, act))

  

dir_sequences = {}

for si in range(len(dirpad)):
    for sj in range(len(dirpad[0])):
        if numpad[si][sj] != "-":
            queue = deque()
            seen = set()
            queue.append(Node((si, sj), None, ""))
            seen.add((si, sj))
            while queue:
                curr = queue.popleft()
                this = deepcopy(curr)
                pos = curr.pos
                seen.add(pos)
                sequence = ""
                while curr:
                    sequence += curr.prev_action
                    curr = curr.prev_node
                sequence = sequence[::-1]
                if dir_changes(sequence) <= 1:
                    if ((si, sj), (pos)) in dir_sequences.keys():
                        dir_sequences[((si, sj), (pos))].append(sequence + "A")
                    else:
                        dir_sequences[((si, sj), (pos))] = [sequence + "A"]           
                neighs = get_neighbours(pos[0], pos[1], dir_bounds)
                for act, neigh in neighs:
                    if neigh not in seen:
                        queue.append(Node((neigh[0], neigh[1]), this, act))

num_poss = {}
for i in range(len(numpad)):
    for j in range(len(numpad[0])):
        num_poss[numpad[i][j]] = (i, j) 

dir_poss = {}
for i in range(len(dirpad)):
    for j in range(len(dirpad[0])):
        dir_poss[dirpad[i][j]] = (i, j)
    
data = data.split("\n")

@functools.cache
def poss_numpad(code, pos, moves):
    if code == "":
        return [moves]
    next_pos = num_poss[code[0]]
    outcomes = []
    for path in num_sequences[(pos, next_pos)]:
        res = poss_numpad(code[1:], next_pos, moves + path)
        best_len = float('inf')
        for o in res:
            outcomes.append(o)
    return outcomes


pos_char = {}
for i in range(2):
    for j in range(3):
        pos_char[i, j] = dirpad[i][j]

import random

best_dirs = {}
for si in range(2):
    for sj in range(3):
        for ei in range(2):
            for ej in range(3):
                right, left, up, down = max(0, ej - sj), max(0, sj - ej), max(0, si - ei), max(0, ei - si)
                path = ">" * right + "^" * up + "v" * down + "<" * left + "A"
                path = "^" * up + ">" * right + "v" * down + "<" * left + "A"
                best_dirs[(si, sj), (ei, ej)] = path
        
        
best_dirs[dir_poss["<"], dir_poss["^"]] = ">^A"
best_dirs[dir_poss["<"], dir_poss["A"]] = ">>^A"




    
    
depth = 25

def evolve(pairs, dic):
    new_pairs = {}
    for pair, count in pairs.items():
        evolved_path = dic[pair]
        pos = dir_poss["A"]
        for char in evolved_path:
            next_pos = dir_poss[char]
            if (pos, next_pos) in new_pairs.keys():
                new_pairs[pos, next_pos] += count
            else:
                new_pairs[pos, next_pos] = count
            pos = next_pos
    return new_pairs


dir_dicts = []
dir_dicts.append(best_dirs)
for pair, options in dir_sequences.items():
    if pair[0] != (0, 0):
        if len(options) > 1:
            new_dirs = []
            for dir in dir_dicts:
                for option in options:
                    new_dir = deepcopy(dir)
                    new_dir[pair] = option
                    new_dirs.append(new_dir)
            dir_dicts = new_dirs
    

totals = []
for dic in dir_dicts:
    total = 0
    for line in data:
        weight = int(line[0:len(line)-1])
        paths = poss_numpad(line, num_poss["A"], "")
        pairs = []
        
        # get initial pairs
        for path in paths:
            pair_count = {}
            read = {}
            pos = dir_poss["A"]
            for char in path:
                next_pos = dir_poss[char]
                if (pos, next_pos) in pair_count.keys():
                    pair_count[pos, next_pos] += 1
                else:
                    pair_count[pos, next_pos] = 1
                pos = next_pos
            pairs.append(pair_count)
        
        i = 0
        while i < depth:
            next_pairs = []
            for pair_count in pairs:
                pair_count = evolve(pair_count, dic)
                next_pairs.append(pair_count)
            pairs = next_pairs
            i += 1
            
        # calculate result
        shortest_len = float("inf")
        for pair_count in pairs:
            l = sum(count for count in pair_count.values())
            if l < shortest_len:
                shortest_len = l
        total += shortest_len * weight
    totals.append(total)
print(min(totals))