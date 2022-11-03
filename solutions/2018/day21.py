from dis import Instruction
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

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Chronal Conversion"
        self.input = self.getInput(self.day)

        self.ir = None
        self.program = None

    def load_program(self):
        lines = self.input.splitlines()
        ip_line = lines[0]
        self.ir = int(ip_line.split(' ')[1])

        self.program = []
        for line in lines[1:]:
            instruction = line.split(' ')
            for i in range(1, len(instruction)):
                instruction[i] = int(instruction[i])

            self.program.append(tuple(instruction))
        
        return self.program

    def run(self, registers, p1):
        ip = 0
        last = None
        seen = set()
        while ip >= 0 and ip < len(self.program):
            registers[self.ir] = ip

            instruction = self.program[ip]
            registers = INSTRUCTIONS[instruction[0]](registers, instruction[1], instruction[2], instruction[3])

            if p1 and ip == len(self.program) - 1:
                return max(registers)

            if ip == len(self.program) - 1:
                has_seen = registers[2] in seen
                if not has_seen:
                    seen.add(registers[2])
                    last = registers[2]
                else:
                    return last

            ip = registers[self.ir]
            ip += 1

        return registers

    def solve(self):
        start_time = time()

        self.load_program()
        
        part1 = self.run([0, 0, 0, 0, 0, 0], True)

        self.printRow((self.day, self.title, part1, '', ''))

        part2 = self.run([0, 0, 0, 0, 0, 0], False)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
