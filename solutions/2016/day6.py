from typing import Counter
from Table import Table
from time import time

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Signals and Noise"
        self.input = self.getInput(self.day)

    def get_columns(self):
        cols = {}
        for i, _ in enumerate(self.input.splitlines()[0]):
            cols[i] = []
        
        for line in self.input.splitlines():
            for i, char in enumerate(line):
                cols[i].append(char)

        return cols

    def solve(self):
        start_time = time()

        cols = self.get_columns()

        word1 = []
        word2 = []
        for key in cols:
            count = Counter(cols[key])
            word1.append(count.most_common()[0][0])
            word2.append(count.most_common()[-1][0])

        part1 = "".join(word1)
        part2 = "".join(word2)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
