from Table import Table
from time import time

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Let It Snow"
        self.input = self.getInput(self.day)

    def get_location(self):
        words = self.input.split(" ")

        row = int(words[-3].strip()[:-1])
        column = int(words[-1].strip()[:-1])

        return (row, column)

    def next(self, location):
        if location[0] == 1:
            return (location[1] + 1, 1)

        return (location[0] - 1, location[1] + 1)


    def find(self, location: tuple, grid: dict):
        current = (1,1)

        while True:
            prev = current
            current = self.next(prev)

            grid[current] = (grid[prev] * 252533) % 33554393

            if current == location:
                return grid[current]

    def solve(self):
        start_time = time()

        location = self.get_location()
        grid = { (1,1): 20151125 }

        part1 = self.find(location, grid)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, "Finished!", seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
