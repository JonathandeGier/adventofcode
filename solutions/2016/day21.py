from tkinter import Y
from Table import Table
from time import time

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Scrambled Letters and Hash"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        # Instructions:
        # ('swap', 'position', X, Y)
        # ('swap', 'letter', X, Y)
        # ('rotate', 'left', X)
        # ('rotate', 'right', X)
        # ('rotate', 'based', X)
        # ('reverse', X, Y)
        # ('move', X, Y)
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(' ')

            if segments[0] == 'swap':
                instructions.append((segments[0], segments[1], self.try_to_int(segments[2]), self.try_to_int(segments[5])))
            elif segments[0] == 'rotate':
                if segments[1] == 'based':
                    x = segments[6]
                else:
                    x = segments[2]

                instructions.append((segments[0], segments[1], self.try_to_int(x)))
            elif segments[0] == 'reverse':
                instructions.append((segments[0], self.try_to_int(segments[2]), self.try_to_int(segments[4])))
            elif segments[0] == 'move':
                instructions.append((segments[0], self.try_to_int(segments[2]), self.try_to_int(segments[5])))
            else:
                assert False, 'Unknown instruction: ' + segments[0]
        
        return instructions


    def try_to_int(self, val):
        try:
            return int(val)
        except:
            return val

    def swapPosition(self, string: str, x_i, y_i):
        y = string[y_i]
        string = string[:y_i] + string[x_i] + string[y_i + 1:]
        string = string[:x_i] + y + string[x_i + 1:]

        return string

    def swapLetter(self, string: str, x, y):
        string = string.replace(x, '-', 1)
        string = string.replace(y, x, 1)
        string = string.replace('-', y)

        return string

    def rotateLeft(self, string: str, steps: int):
        return string[steps:] + string[:steps]

    def rotateRight(self, string: str, steps: int):
        steps = len(string) - steps

        return string[steps:] + string[:steps]

    def rotateBased(self, string: str, letter):
        i = string.find(letter)

        steps = 1 + i
        if i >= 4:
            steps += 1

        return self.rotateRight(string, steps)

    def reverse(self, string: str, x: int, y: int):
        if x > 0:
            return string[:x] + string[y:x - 1:-1] + string[y+1:]
        else:
            return string[y::-1] + string[y+1:]

    def move(self, string: str, x_i: int, y_i: int):
        x = string[x_i]
        string = string[:x_i] + string[x_i + 1:]

        return string[:y_i] + x + string[y_i:]

    def scramble(self, string: str, instructions):

        for instruction in instructions:
            if instruction[0] == 'swap' and instruction[1] == 'position':
                string = self.swapPosition(string, instruction[2], instruction[3])

            elif instruction[0] == 'swap' and instruction[1] == 'letter':
                string = self.swapLetter(string, instruction[2], instruction[3])

            elif instruction[0] == 'rotate' and instruction[1] == 'left':
                string = self.rotateLeft(string, instruction[2])

            elif instruction[0] == 'rotate' and instruction[1] == 'right':
                string = self.rotateRight(string, instruction[2])

            elif instruction[0] == 'rotate' and instruction[1] == 'based':
                string = self.rotateBased(string, instruction[2])

            elif instruction[0] == 'reverse':
                string = self.reverse(string, instruction[1], instruction[2])

            elif instruction[0] == 'move':
                string = self.move(string, instruction[1], instruction[2])

            else:
                assert False, 'unknown instruction: ' + instruction[0]

        return string

    def unscramble(self, string: str, instructions):

        instructions = instructions[::-1]

        for instruction in instructions:
            if instruction[0] == 'swap' and instruction[1] == 'position':
                string = self.swapPosition(string, instruction[2], instruction[3])

            elif instruction[0] == 'swap' and instruction[1] == 'letter':
                string = self.swapLetter(string, instruction[2], instruction[3])

            elif instruction[0] == 'rotate' and instruction[1] == 'left':
                string = self.rotateRight(string, instruction[2])

            elif instruction[0] == 'rotate' and instruction[1] == 'right':
                string = self.rotateLeft(string, instruction[2])

            elif instruction[0] == 'rotate' and instruction[1] == 'based':
                for shift in range(len(string)):
                    testString = self.rotateLeft(string, shift)

                    if string == self.rotateBased(testString, instruction[2]):
                        string = testString
                        break

            elif instruction[0] == 'reverse':
                string = self.reverse(string, instruction[1], instruction[2])

            elif instruction[0] == 'move':
                string = self.move(string, instruction[2], instruction[1])

            else:
                assert False, 'unknown instruction: ' + instruction[0]

        return string

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        part1 = self.scramble('abcdefgh', instructions)
        part2 = self.unscramble('fbgdceah', instructions)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
