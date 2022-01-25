from typing import Counter
from itertools import combinations
from Table import Table
from time import time

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "No Such Thing as Too Much"
        self.input = self.getInput(self.day)

    def get_sizes(self):
        lines = self.input.splitlines()
        return [int(x) for x in lines]

    def solve(self):
        start_time = time()

        containers = self.get_sizes()
        target = 150

        result = [seq for i in range(len(containers), 0, -1)
            for seq in combinations(containers, i)
            if sum(seq) == target]

        part1 = len(result)

        count = Counter([len(x) for x in result])
        lowest_key = min(count.keys())
        part2 = count[lowest_key]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
