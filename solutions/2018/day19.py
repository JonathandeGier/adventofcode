from itertools import chain
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

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Go With The Flow"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            instruction = line.split(' ')
            for i in range(1, len(instruction)):
                instruction[i] = int(instruction[i])

            instructions.append(tuple(instruction))
        
        return instructions

    def run(self, instructions, registers):
        ip = 0
        ir = instructions[0][1]

        instructions = instructions[1:]

        while ip >= 0 and ip < len(instructions):
            registers[ir] = ip

            # if we are on the last instruction, meaning part 2, we run optimized code
            if ip == len(instructions) - 1:
                val = max(registers)
                result = sum(set(chain.from_iterable((i, val // i) for i in range(1, int(val**0.5) + 1) if not val % i)))
                registers[0] = result
                return registers

            instruction = instructions[ip]
            registers = INSTRUCTIONS[instruction[0]](registers, instruction[1], instruction[2], instruction[3])

            ip = registers[ir]
            ip += 1

        return registers

    def run_part_2(self, n):
        return sum(set(chain.from_iterable((i, n // i) for i in range(1, int(n**0.5) + 1) if not n % i)))

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        result_registers = self.run(instructions, [0, 0, 0, 0, 0, 0])
        part1 = result_registers[0]

        result_registers = self.run(instructions, [1, 0, 0, 0, 0, 0])
        part2 = result_registers[0]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
