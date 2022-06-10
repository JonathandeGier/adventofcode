import math
from Table import Table
from time import time

class Generator:

    def __init__(self, start_value, factor, mod):
        self.value = start_value
        self.factor = factor
        self.mod = mod

    def next(self, p2 = False):
        self.value = self.value * self.factor % 2147483647

        if p2:
            while self.value % self.mod != 0:
                self.value = self.value * self.factor % 2147483647

        return self.value

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Dueling Generators"
        self.input = self.getInput(self.day)

    def get_generators(self):
        lines = self.input.splitlines()

        genA = Generator(int(lines[0].split(' ')[-1]), 16807, 4)
        genB = Generator(int(lines[1].split(' ')[-1]), 48271, 8)

        return genA, genB

    def solve(self):
        start_time = time()

        genA, genB = self.get_generators()

        pairs = 0
        for i in range(40000000):
            if i % 100000 == 0:
                per = (i / 40000000) * 100
                percentage = str(round(per, 1)) + ' %'
                self.printRow((self.day, self.title, percentage, '', ''), end="\r")

            valA = genA.next()
            valB = genB.next()

            if (valA & 0xFFFF) == (valB & 0xFFFF):
                pairs += 1

        part1 = pairs

        pairs = 0
        genA, genB = self.get_generators()

        for i in range(5000000):
            if i % 10000 == 0:
                per = (i / 5000000) * 100
                percentage = str(round(per, 1)) + ' %'
                self.printRow((self.day, self.title, part1, percentage, ''), end="\r")

            valA = genA.next(True)
            valB = genB.next(True)

            if (valA & 0xFFFF) == (valB & 0xFFFF):
                pairs += 1

        part2 = pairs

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
