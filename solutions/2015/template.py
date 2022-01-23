# Old template
from getInput import get_input

def get_lines():
    input = get_input(2015, 0)


def main():
    print("Puzzle 1:")

    print("")

    print("Puzzle 2:")


if __name__ == "__main__":
    main()

# Table template
from Table import Table
from time import time

class Day0(Table):

    def __init__(self):
        self.day = 0
        self.title = ""
        self.input = Table.getInput(self.day)

    def get_lines(self):
        lines = self.input.splitlines()
        return lines

    def solve(self):
        start_time = time()

        part1 = 0


        part2 = 0

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day0()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
