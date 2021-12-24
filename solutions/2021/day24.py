import numpy
from getInput import get_input
from itertools import product
from math import floor

def get_instructions():
    input = get_input(2021, 24).splitlines()
    instructions = []
    for line in input:
        parts = line.split()
        if parts[0] != "inp":
            try:
                parts[2] = int(parts[2])
            except:
                pass
            instruction = (parts[0], parts[1], parts[2])
        else:
            instruction = (parts[0], parts[1])
        instructions.append(instruction)
    return instructions


def run_program(program, number):
    state = {
        "x": 0,
        "y": 0,
        "z": 0,
        "w": 0,
    }

    for instruction in program:
        if instruction[0] == "inp":
            if number >= 10:
                val = int(str(number)[:1])
                number = int(str(number)[1:])
            else:
                val = number
            state[instruction[1]] = val
        elif instruction[0] == "add":
            val1 = state[instruction[1]]
            if type(instruction[2]) == int:
                val2 = instruction[2]
            else:
                val2 = state[instruction[2]]
            state[instruction[1]] = val1 + val2
        elif instruction[0] == "mul":
            val1 = state[instruction[1]]
            if type(instruction[2]) == int:
                val2 = instruction[2]
            else:
                val2 = state[instruction[2]]
            state[instruction[1]] = val1 * val2
        elif instruction[0] == "div":
            val1 = state[instruction[1]]
            if type(instruction[2]) == int:
                val2 = instruction[2]
            else:
                val2 = state[instruction[2]]
            assert val2 > 0, val2
            state[instruction[1]] = floor(val1 / val2)
        elif instruction[0] == "mod":
            val1 = state[instruction[1]]
            if type(instruction[2]) == int:
                val2 = instruction[2]
            else:
                val2 = state[instruction[2]]
            state[instruction[1]] = val1 % val2
        elif instruction[0] == "eql":
            val1 = state[instruction[1]]
            if type(instruction[2]) == int:
                val2 = instruction[2]
            else:
                val2 = state[instruction[2]]
            if val1 == val2:
                state[instruction[1]] = 1
            else:
                state[instruction[1]] = 0
        else:
            assert False, "Unknown instruction: " + instruction[0]
    
    return state["z"] == 0

def guess():
    
    # Max
    # W = [  5,  9,  9,  9,   8,   4,  2,  6,  9,  9,  7,  9,   9,  9 ]

    # Min
    #      0   1   2   3    4    5   6   7   8   9  10  11   12  13
    W = [  1,  3,  6,  2,   1,   1,  1,  1,  4,  9,  1,  3,   1,  5 ]

    # user specific code variables
    Z = (  1,  1,  1,  1,  26,  26,  1,  1, 26, 26,  1, 26,  26, 26 )
    X = ( 13, 12, 12, 10, -11, -13, 15, 10, -2, -6, 14,  0, -15, -4 )
    Y = (  8, 13,  8, 10,  12,   1, 13,  5, 10,  3,  2,  2,  12,  7 )

    while True:
        x = 0
        y = 0
        z = 0
        for i in range(14):
            z26 = z % 26
            goal = z26 + X[i]
            if 1 <= goal <= 9:
                W[i] = goal
            
            z //= Z[i]
            x = (0 if W[i]==goal else 1)
            z *= (25 if x==1 else 0) + 1
            z += (W[i] + Y[i] if x == 1 else 0)
            print(f'i={i:2}  goal={goal:2}  z26={z26:2}  X[i]={X[i]:3}  Y={Y[i]:2}  W={W[i]:1}  Z={Z[i]:2}  z={[(z//26**i)%26 for i in range(14)]}')
            if X[i] < 10 and W[i] != goal:
                break
        print(W, z, "".join([str(x) for x in W]), i)
        if z == 0:
            return True
        return False


def main():
    instructions = get_instructions()
    guess()


if __name__ == "__main__":
    main()
