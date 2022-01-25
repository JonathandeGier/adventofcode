from itertools import groupby
from Table import Table
from time import time

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Elves Look, Elves Say"
        self.input = self.getInput(self.day)

    def get_number(self):
        return self.input.strip()

    def calculate(self, number, iterations):
        for _ in range(iterations):
            next = ""
            seq = ["".join(g) for k, g in groupby(number)]
            for n in seq:
                next += str(len(n))
                next += n[0]
            number = next
        return number

    def solve(self):
        start_time = time()

        number = self.get_number()
        part1 = len(self.calculate(number, 40))

        number = self.get_number()
        part2 = len(self.calculate(number, 50))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
