from collections import deque
from Table import Table
from time import time

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "Duet"
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

    def get_value(self, input, registers):
        if type(input) == int:
            return input
        elif input in registers:
            return registers[input]
        else:
            registers[input] = 0
            return 0

    def run(self, instructions):

        registers = {}
        sounds = []

        i = 0
        while True:
            if i < 0 or i >= len(instructions):
                break

            instruction = instructions[i]

            if instruction[0] == 'snd':
                sounds.append(self.get_value(instruction[1], registers))
            elif instruction[0] == 'set':
                self.get_value(instruction[1], registers)
                registers[instruction[1]] = self.get_value(instruction[2], registers)
            elif instruction[0] == 'add':
                self.get_value(instruction[1], registers)
                registers[instruction[1]] += self.get_value(instruction[2], registers)
            elif instruction[0] == 'mul':
                self.get_value(instruction[1], registers)
                registers[instruction[1]] = registers[instruction[1]] * self.get_value(instruction[2], registers)
            elif instruction[0] == 'mod':
                self.get_value(instruction[1], registers)
                registers[instruction[1]] = registers[instruction[1]] % self.get_value(instruction[2], registers)
            elif instruction[0] == 'rcv':
                self.get_value(instruction[1], registers)
                if registers[instruction[1]] != 0:
                    break
            elif instruction[0] == 'jgz':
                self.get_value(instruction[1], registers)
                if registers[instruction[1]] > 0:
                    i += self.get_value(instruction[2], registers) - 1
            else:
                assert False

            i += 1

        return registers, sounds

    def step(self, program, instruction, i, registers, queue, otherProgram):

        if program == 0:
            agfrg = 3

        if instruction[0] == 'snd':
            queue[otherProgram].append(self.get_value(instruction[1], registers))
            registers['send_val'] += 1
        elif instruction[0] == 'set':
            if instruction[1] not in registers:
                registers[instruction[1]] = 0

            registers[instruction[1]] = self.get_value(instruction[2], registers)
        elif instruction[0] == 'add':
            if instruction[1] not in registers:
                registers[instruction[1]] = 0

            registers[instruction[1]] += self.get_value(instruction[2], registers)
        elif instruction[0] == 'mul':
            if instruction[1] not in registers:
                registers[instruction[1]] = 0

            registers[instruction[1]] = registers[instruction[1]] * self.get_value(instruction[2], registers)
        elif instruction[0] == 'mod':
            if instruction[1] not in registers:
                registers[instruction[1]] = 0

            registers[instruction[1]] = registers[instruction[1]] % self.get_value(instruction[2], registers)
        elif instruction[0] == 'rcv':
            if len(queue[program]) > 0:
                registers[instruction[1]] = queue[program].popleft()
            else:
                i -= 1
        elif instruction[0] == 'jgz':
            if self.get_value(instruction[1], registers) > 0:
                i += self.get_value(instruction[2], registers) - 1
        else:
            assert False

        i += 1

        return i, registers, queue

    def duet(self, instructions):

        queue = {
            0: deque(),
            1: deque(),
        }

        i0 = 0
        terminated0 = False
        waiting0 = False
        registers0 = {
            'p': 0,
            'send_val': 0,
        }

        i1 = 0
        terminated1 = False
        waiting1 = False
        registers1 = {
            'p': 1,
            'send_val': 0,
        }

        while True:
            
            if not terminated0:
                old_i0 = i0
                i0, registers0, queue = self.step(0, instructions[i0], i0, registers0, queue, 1)
                
                if i0 < 0 or i0 >= len(instructions):
                    terminated0 = True

                waiting0 = old_i0 == i0

            if not terminated1:
                old_i1 = i1
                i1, registers1, queue = self.step(1, instructions[i1], i1, registers1, queue, 0)

                if i1 < 0 or i1 >= len(instructions):
                    terminated1 = True

                waiting1 = old_i1 == i1

            if waiting0 and waiting1:
                terminated0 = True
                terminated1 = True

            if waiting0 and terminated1:
                terminated0 = True

            if waiting1 and terminated0:
                terminated1 = True

            if terminated0 and terminated1:
                break

        return registers1['send_val']


    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        registers, sounds = self.run(instructions)

        part1 = sounds[-1]


        part2 = self.duet(instructions)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
