from dis import Instruction
from msilib.schema import InstallUISequence

from jsii import enum
from Table import Table
from time import time

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Two-Factor Authentication"
        self.input = self.getInput(self.day)
        
        self.display = []
        self.init_display()

    def init_display(self):
        for _ in range(6):
            row = []
            for _ in range(50):
                row.append(False)
            self.display.append(row)

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(" ")
            if segments[0] == "rect":
                numbers = segments[1].split("x")
                instructions.append((segments[0], int(numbers[0]), int(numbers[1])))
            elif segments[0] == "rotate":
                instructions.append((segments[1], int(segments[2][2:]), int(segments[-1])))
            else:
                assert False, "Unknown instruction"

        return instructions

    def apply_instruction(self, instruction: tuple):
        if instruction[0] == "rect":
            for column in range(instruction[1]):
                for row in range(instruction[2]):
                    self.display[row][column] = True
        elif instruction[0] == "row":
            row = self.display[instruction[1]]
            new_row = [False for _ in range(50)]
            for i, val in enumerate(row):
                new_i = i + instruction[2]
                if new_i > 49:
                    new_i -= 50
                new_row[new_i] = val

            self.display[instruction[1]] = new_row
        elif instruction[0] == "column":
            column = [row[instruction[1]] for row in self.display]
            new_column = [False for _ in range(6)]
            for i, val in enumerate(column):
                new_i = i + instruction[2]
                if new_i > 5:
                    new_i -= 6
                new_column[new_i] = val

            for i, val in enumerate(new_column):
                self.display[i][instruction[1]] = val
        else:
            assert False, "Unknown instruction"

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()
        
        for instruction in instructions:
            self.apply_instruction(instruction)

        part1 = sum([sum(row) for row in self.display])

        # todo: decode the display result
        part2 = "EFEYKFRFIJ"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def print_display(self):
        def pixel(val: bool):
            if val:
                return "#"
            else:
                return " "

        for row in self.display:
            print("".join([pixel(val) for val in row]))


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
    day.print_display()
    print("")
