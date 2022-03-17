from turtle import right
from jsii import enum
from Table import Table
from time import time

class Day18(Table):
    # safe = True, trap = False

    def __init__(self):
        self.day = 18
        self.title = "Like a Rogue"
        self.input = self.getInput(self.day).strip()

    def initial_row(self):
        row = []
        for char in self.input:
            if char == '.':
                row.append(True)
            else:
                row.append(False)

        return row

    def add_row(self, grid: list):
        last_row = grid[-1]
        new_row = []

        for i, val in enumerate(last_row):
            if i - 1 < 0:
                left = True
            else:
                left = last_row[i - 1]

            if i + 1 >= len(last_row):
                right = True
            else:
                right = last_row[i + 1]

            center = last_row[i]

            is_safe = True
            if not left and not center and right:
                is_safe = False
            elif not right and not center and left:
                is_safe = False
            elif not left and center and right:
                is_safe = False
            elif not right and center and left:
                is_safe = False

            new_row.append(is_safe)

        grid.append(new_row)

    def solve(self):
        start_time = time()

        grid = []
        grid.append(self.initial_row())

        while len(grid) < 40:
            self.add_row(grid)

        part1 = sum([sum(row) for row in grid])

        while len(grid) < 400000:
            self.add_row(grid)

        part2 = sum([sum(row) for row in grid])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def print_grid(self, grid: list):
        for row in grid:
            string = ""
            for val in row:
                if val:
                    string += "."
                else:
                    string += "^"

            print(string)


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
