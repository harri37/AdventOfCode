data = "773 79858 0 71 213357 2937 1 3998391"
data = [int(x) for x in data.split(" ")]

from collections import Counter

def evolve(num):
    str_val = str(num)
    if len(str_val) % 2 == 0:
        return [int(str_val[:(len(str_val)//2)]), int(str_val[(len(str_val)//2):])]
    elif num == 0:
        return [1]
    else:
        return [num * 2024]

n = 75
curr_freq = Counter(data)

for it in range(n):
    next_freq = {}
    for num, amount in curr_freq.items():
        evolved = evolve(num)
        for res in evolved:
            if res in next_freq:
                next_freq[res] += amount
            else:
                next_freq[res] = amount
    curr_freq = next_freq

print(sum(curr_freq.values()))
