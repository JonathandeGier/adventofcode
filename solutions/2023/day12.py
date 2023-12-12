from Table import Table
from time import time
from itertools import product

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = ""
        self.input = self.getInput(self.day)

    def parse_lines(self):
        records = []
        for line in self.input.splitlines():
            data, sequence = line.split(' ')
            records.append((data, tuple([int(x) for x in sequence.split(',')])))
        return records

    def possible(self, data: str, sequence: tuple) -> bool:
        data_sequence = tuple([len(x) for x in data.split('.') if len(x) != 0])
        return data_sequence == sequence

    def possebilities(self, data: str, sequence: tuple):
        possebilities = []

        unknown = len([x for x in data if x == '?'])
        for sub in product('#.', repeat=unknown):
            restored_data = data
            for char in sub:
                i = restored_data.index('?')
                assert i != -1
                restored_data = restored_data[:i] + char + restored_data[i+1:]

            if self.possible(restored_data, sequence):
                possebilities.append(restored_data)
        return possebilities



    def solve(self):
        start_time = time()

        records = self.parse_lines()

        part1 = sum([len(self.possebilities(data, sequence)) for data, sequence in records])
        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
