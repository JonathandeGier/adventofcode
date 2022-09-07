from Table import Table
from time import time
from multiprocessing import Pool

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "Alchemical Reduction"
        self.input = self.getInput(self.day)

    def reduce(self, polymer: list):
        i = 0
        while i < len(polymer) - 1:
            if polymer[i].lower() == polymer[i+1].lower() and polymer[i] != polymer[i+1]:
                del polymer[i+1]
                del polymer[i]
                i = -1
            i += 1
        return len(polymer)

    def solve(self):
        start_time = time()

        self.printRow((self.day, self.title, '', '', ''), end='\r')

        polymer = self.input.splitlines()[0]

        part1 = self.reduce(list(polymer))
        self.printRow((self.day, self.title, part1, 'Multiprocessing...', ''), end='\r')

        with Pool(8) as p:
            results = p.map(self.reduce, [list(polymer.replace(chr(i), '').replace(chr(i).upper(), '')) for i in range(97, 123)])

        part2 = min(results)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
