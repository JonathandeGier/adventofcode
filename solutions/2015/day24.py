from itertools import combinations
from Table import Table
from time import time

class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "It Hangs in the Balance"
        self.input = self.getInput(self.day)

    def get_packages(self):
        return [int(x) for x in self.input.splitlines()]

    def product(self, items: list):
        product = 1
        for item in items:
            product *= item
        return product

    def solve(self):
        start_time = time()

        packages = self.get_packages()
        target = sum(packages) // 3

        i = 0
        while True:
            i += 1
            groups = []
            for group in combinations(packages, i):
                if sum(group) == target:
                    groups.append(group)
            if len(groups) > 0:
                break

        group_lengths = [len(x) for x in groups]
        smallest_groups = []
        for group in groups:
            if len(group) == min(group_lengths):
                smallest_groups.append(group)

        quantum_entanglement = [self.product(x) for x in smallest_groups]
        
        part1 = min(quantum_entanglement)


        target = sum(packages) // 4
        
        i = 0
        while True:
            i += 1
            groups = []
            for group in combinations(packages, i):
                if sum(group) == target:
                    groups.append(group)
            if len(groups) > 0:
                break

        group_lengths = [len(x) for x in groups]
        smallest_groups = []
        for group in groups:
            if len(group) == min(group_lengths):
                smallest_groups.append(group)

        quantum_entanglement = [self.product(x) for x in smallest_groups]
        
        part2 = min(quantum_entanglement)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
