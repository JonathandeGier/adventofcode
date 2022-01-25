from Table import Table
from time import time

class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "Opening the Turing Lock"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        instructions = []

        for line in self.input.splitlines():
            instructions.append((line[:3].strip(), line[4:].strip()))

        return instructions

    def run(self, instructions, registers):
        i = 0
        while True:
            if i >= len(instructions):
                break

            instruction = instructions[i]

            if instruction[0] == "inc":
                registers[instruction[1]] += 1
            elif instruction[0] == "hlf":
                registers[instruction[1]] = registers[instruction[1]] / 2
            elif instruction[0] == "tpl":
                registers[instruction[1]] = registers[instruction[1]] * 3
            elif instruction[0] == "jmp":
                i += int(instruction[1])
                continue
            elif instruction[0] == "jie":
                parts = instruction[1].split(",")
                reg = parts[0].strip()
                offset = parts[1].strip()

                if registers[reg] % 2 == 0:
                    i += int(offset)
                    continue
            elif instruction[0] == "jio":
                parts = instruction[1].split(",")
                reg = parts[0].strip()
                offset = parts[1].strip()

                if registers[reg] == 1:
                    i += int(offset)
                    continue

            i += 1

        return registers

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        results = self.run(instructions, { "a": 0, "b": 0 })
        part1 = results["b"]


        results = self.run(instructions, { "a": 1, "b": 0 })
        part2 = results["b"]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
