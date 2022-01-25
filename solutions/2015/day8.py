import ast
from Table import Table
from time import time

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Matchsticks"
        self.input = self.getInput(self.day)

    def get_strings(self):
        input = self.input.splitlines()
        return input

    def len_in_code(self, string):
        return len(string)

    def len_chars(self, string):
        return len(ast.literal_eval(string))

    def len_encoded(self, string: str):
        new_string = '"'
        for char in string:
            if char == "\\" or char == '"':
                new_string += "\\"
            new_string += char
        new_string += '"'

        return len(new_string)

    def solve(self):
        start_time = time()

        strings = self.get_strings()

        part1 = 0
        for string in strings:
            part1 += self.len_in_code(string)
            part1 -= self.len_chars(string)

        part2 = 0
        for string in strings:
            part2 += self.len_encoded(string)
            part2 -= self.len_in_code(string)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
