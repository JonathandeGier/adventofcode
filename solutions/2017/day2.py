from posixpath import split
from Table import Table
from time import time

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Corruption Checksum"
        self.input = self.getInput(self.day)

    def get_grid(self):
        grid = []
        for row in self.input.splitlines():
            grid.append([int(val) for val in row.split("\t")])

        return grid

    def solve(self):
        start_time = time()

        grid = self.get_grid()

        part1 = sum([max(row) - min(row) for row in grid])

        part2 = 0
        for row in grid:
            row_completed = False
            for i in range(len(row)):
                for j in range(len(row)):
                    if i == j:
                        continue

                    if row[i] % row[j] == 0:
                        part2 += row[i] // row[j]
                        row_completed = True
                        break

                if row_completed:
                    break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
