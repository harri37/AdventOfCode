import re

split1 = data.split("mul")

def prod(s):
    if len(s) < 5:
        return 0
    if s[0] != '(':
        return 0
    if s.count(')') < 1:
        return 0
    s = s.split(')')[0]
    s = s[1:]
    nums = s.split(',')
    if len(nums) != 2:
        return 0
    if not nums[0].isdigit() or not nums[1].isdigit():
        return 0
    return int(nums[0]) * int(nums[1])

ress = [prod(x) for x in split1]
print(sum(ress))

split2 = re.split("do|mul", data)

def eval(s):
    if s[:2] == "()":
        return 1
    if s[:5] == "n't()":
        return -1
    else:
        return prod(s)

evals = [eval(s) for s in split2]
do = 1
sum_result = 0

for val in evals:
    if val == 1:
        do = 1
    elif val == -1:
        do = 0
    else:
        sum_result += do * val

print(sum_result)