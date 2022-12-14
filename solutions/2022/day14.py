from Table import Table
from time import time

WALL = '#'

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Regolith Reservoir"
        self.input = self.getInput(self.day)

        self.map = {}

    def load_map(self):
        self.map = {}
        for line in self.input.splitlines():
            coordinates = [tuple([int(val) for val in coor.split(',')]) for coor in line.split(' -> ')]
            
            for i in range(len(coordinates) - 1):
                _from = coordinates[i]
                _to = coordinates[i+1]

                min_x = min(_from[0], _to[0])
                max_x = max(_from[0], _to[0])
                min_y = min(_from[1], _to[1])
                max_y = max(_from[1], _to[1])

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        self.map[x, y] = WALL

    def solve(self):
        start_time = time()

        self.load_map()

        part1 = "None"
        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
