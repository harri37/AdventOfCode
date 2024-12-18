data = """Register A: 64584136
Register B: 0
Register C: 0

Program: 2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0"""


import re

registers, program = data.split("\n\n")

register_vals = {}

register_pattern = r"Register\s([A-Z]):\s(\d+)"

matches = re.findall(register_pattern, registers)

for name, val in matches:
    register_vals[name] = int(val)

_, program = program.split(" ")
program = [int(op) for op in program.split(",")]

output = []

def combo_op(op):
    if 0 <= op <= 3:
        return op
    elif op == 4:
        return register_vals['A']
    elif op == 5:
        return register_vals['B']
    elif op == 6:
        return register_vals['C']

def adv(op):
    register_vals['A'] = register_vals['A'] // (2 ** combo_op(op))
    
def bxl(op):
    register_vals['B'] = register_vals['B'] ^ op
    
def bst(op):
    register_vals['B'] = combo_op(op) % 8
    
def jnz(op):
    if register_vals['A'] != 0:
        return op
    else:
        return None

def bxc(op):
    register_vals['B'] = register_vals['B'] ^ register_vals['C']
    
def out(op):
    output.append(combo_op(op) % 8)
    
def bdv(op):
    register_vals['B'] = register_vals['A'] // (2 ** combo_op(op))

def cdv(op):
    register_vals['C'] = register_vals['A'] // (2 ** combo_op(op))

instructions = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


i = 0
while i + 1 < len(program):
    operation, operand = program[i], program[i +1]
    if operation == 3:
        jump = instructions[operation](operand)
        if jump is not None:
            i = jump
        else:
            i += 2
    else:
        instructions[operation](operand)
        i += 2
print(",".join([str(o) for o in output]))

# PART 2

def run_program(A):
    B, C = 0, 0
    output = []
    while A > 0:
        B = (A % 8) ^ 2 
        C = A // (2 ** ((A % 8) ^ 2))
        B = B ^ 3 ^ C 
        output.append(B % 8) 
        A = A // 8
    return output

program = list(reversed(program))
possible_A = list(range(1, 8))
i = 1
while i < len(program):
    next_possible = []
    for a in possible_A:
        output = list(reversed(run_program(a)))
        if output == program[:i]:
            for _a in range(8 * a, 8 * a + 8):
                next_possible.append(_a)
    possible_A = next_possible
    i += 1

program = list(reversed(program))
for a in possible_A:
    if run_program(a) == program:
        print(a)
        break
