from collections import Counter
from itertools import combinations
from Table import Table
from time import time

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Inventory Management System"
        self.input = self.getInput(self.day)

    def get_ids(self):
        return self.input.splitlines()

    def solve(self):
        start_time = time()

        ids = self.get_ids()

        doubles = 0
        tripples = 0
        for id in ids:
            count = Counter(id).values()

            if 2 in count:
                doubles += 1
            if 3 in count:
                tripples += 1

        part1 = doubles * tripples

        pairs = combinations(ids, 2)
        for pair in pairs:
            assert len(pair[0]) == len(pair[1])

            off = 0
            string = ''
            for i in range(len(pair[0])):
                if pair[0][i] != pair[1][i]:
                    off += 1
                else:
                    string = string + pair[0][i]

            if off == 1:
                break


        part2 = string

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
