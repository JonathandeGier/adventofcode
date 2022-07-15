from Table import Table
from time import time
from math import sqrt

class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "Coprocessor Conflagration"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        def try_to_int(value):
            try:
                return int(value)
            except Exception:
                return value

        instructions = []
        for line in self.input.splitlines():
            segments = line.split()

            a = try_to_int(segments[1])
            b = None
            if len(segments) > 2:
                b = try_to_int(segments[2])

            instructions.append((segments[0], a, b))

        return instructions

    def run(self, instructions, p2 = False):
        registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
            'e': 0,
            'f': 0,
            'g': 0,
            'h': 0,
        }
        def get_value(input):
            if type(input) == int:
                return input
            elif input in registers:
                return registers[input]
            else:
                registers[input] = 0
                return 0

        if p2:
            registers['a'] = 1

        invocations = {
            'set': 0,
            'sub': 0,
            'mul': 0,
            'jnz': 0,
        }

        if p2:
            condition = lambda x: x < 11
        else:
            condition = lambda x: True

        i = 0
        while condition(i):
            if i < 0 or i >= len(instructions):
                break

            instruction = instructions[i]

            if instruction[0] == 'set':
                registers[instruction[1]] = get_value(instruction[2])
                invocations['set'] += 1
            elif instruction[0] == 'sub':
                registers[instruction[1]] = get_value(instruction[1]) - get_value(instruction[2])
                invocations['sub'] += 1
            elif instruction[0] == 'mul':
                registers[instruction[1]] = get_value(instruction[1]) * get_value(instruction[2])
                invocations['mul'] += 1
            elif instruction[0] == 'jnz':
                if get_value(instruction[1]) != 0:
                    i += (get_value(instruction[2]) - 1)
                invocations['jnz'] += 1
            else:
                assert False

            i += 1

        if p2:
            def is_prime(q):
                s = int(sqrt(q))
                for i in range(2, s + 1):
                    if q % i == 0:
                        return False
                return True

            # Actual program is to slow to run. This is what it does rewritten as python code
            return sum(1 if not is_prime(i) else 0 for i in range(registers['b'], registers['c'] + 1, 17))
        else:
            return invocations['mul']


    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        part1 = self.run(instructions)
        part2 = self.run(instructions, True)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
