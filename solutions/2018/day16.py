from itertools import groupby
from Table import Table
from time import time

def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]
    return reg

def addi(reg, a, b, c):
    reg[c] = reg[a] + b
    return reg

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]
    return reg

def muli(reg, a, b, c):
    reg[c] = reg[a] * b
    return reg

def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]
    return reg

def bani(reg, a, b, c):
    reg[c] = reg[a] & b
    return reg

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]
    return reg

def bori(reg, a, b, c):
    reg[c] = reg[a] | b
    return reg

def setr(reg, a, b, c):
    reg[c] = reg[a]
    return reg

def seti(reg, a, b, c):
    reg[c] = a
    return reg

def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0
    return reg

def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0
    return reg

def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0
    return reg

def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0
    return reg

def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0
    return reg

def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0
    return reg

INSTRUCTIONS = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr,
}

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Chronal Classification"
        self.input = self.getInput(self.day)

    def get_data(self):
        raw_tests, program = self.input.split("\n\n\n\n")

        tests = []
        for raw_test in raw_tests.split("\n\n"):
            test_lines = raw_test.splitlines()
            before = tuple(eval(test_lines[0].split(': ')[1]))
            instruction = eval('(' + ', '.join(test_lines[1].split(' ')) + ')')
            after = tuple(eval(test_lines[2].split(': ')[1]))
            
            tests.append((before, instruction, after))

        instructions = []
        for line in program.splitlines():
            instructions.append(eval('(' + ', '.join(line.split(' ')) + ')'))
        
        return tests, instructions

    def behavior(self, test: tuple):
        possible = []
        for opt_code in INSTRUCTIONS:
            registers = list(test[0])
            result = tuple(INSTRUCTIONS[opt_code](registers, test[1][1], test[1][2], test[1][3]))
            
            if test[2] == result:
                possible.append(opt_code)
        
        return possible

    def common_all(self, array: list):
        first = array[0]

        for l in array:
            for item in first:
                if item not in l:
                    first.remove(item)
        return first


    def solve(self):
        start_time = time()

        tests, program = self.get_data()

        more_than_three = 0
        for test in tests:
            if len(self.behavior(test)) >= 3:
                more_than_three += 1

        part1 = more_than_three

        possible_mapping = {}
        grouped_opt_codes = groupby(sorted(tests, key=lambda x: x[1][0]), key=lambda x: x[1][0])
        for key, grouped_tests in grouped_opt_codes:
            possibles = []

            for test in grouped_tests:
                possibles.append(self.behavior(test))
            
            possible_mapping[key] = self.common_all(possibles)        

        mapping = {}
        while len(possible_mapping.keys()) > 0:
            for key in list(possible_mapping.keys()):

                for found in mapping.values():
                    if found in possible_mapping[key]:
                        possible_mapping[key].remove(found)

                if len(possible_mapping[key]) == 1:
                    mapping[key] = possible_mapping[key][0]
                    del possible_mapping[key]

        registers = [0, 0, 0, 0]
        for instruction in program:
            INSTRUCTIONS[mapping[instruction[0]]](registers, instruction[1], instruction[2], instruction[3])

        part2 = registers[0]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
