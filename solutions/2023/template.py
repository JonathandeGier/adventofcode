from Table import Table
from time import time

class Day0(Table):

    def __init__(self):
        self.day = 0
        self.title = ""
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        part1 = "None"
        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day0()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
