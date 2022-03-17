from dis import Instruction
from Table import Table
from time import time

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Leonardo's Monorail"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(' ')
            instructions.append(tuple([self.try_to_int(val) for val in segments]))
        
        return instructions

    def try_to_int(self, val):
        try:
            return int(val)
        except:
            return val

    def run(self, instructions, p2 = False):
        registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
        }

        if p2:
            registers['c'] = 1

        i = 0
        while i < len(instructions):
            instruction = instructions[i]

            if instruction[0] == 'cpy':
                if instruction[1] not in registers:
                    registers[instruction[1]] = instruction[1]
                registers[instruction[2]] = registers[instruction[1]]
            elif instruction[0] == 'inc':
                registers[instruction[1]] += 1
            elif instruction[0] == 'dec':
                registers[instruction[1]] -= 1
            elif instruction[0] == 'jnz':
                if registers[instruction[1]] != 0:
                    i += (instruction[2] - 1)
            else:
                assert False, 'Unknown instruction'

            i += 1

        return registers

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        result = self.run(instructions)
        part1 = result['a']

        result2 = self.run(instructions, True)
        part2 = result2['a']

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
