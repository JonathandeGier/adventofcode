from Table import Table
from time import time

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Not Quite Lisp"
        self.input = Table.getInput(self.day)

    def solve(self):
        start_time = time()
        part1 = self.input.count("(") - self.input.count(")")

        floor = 0
        pos = 0
        for i, val in enumerate(self.input):
            if val == "(":
                floor += 1
            else:
                floor -= 1
            
            if floor == -1:
                pos = i + 1
                break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, pos, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
