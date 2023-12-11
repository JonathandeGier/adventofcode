from Table import Table
from time import time
from itertools import combinations

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Cosmic Expansion"
        self.input = self.getInput(self.day)

        self.map = {}

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val != '.':
                    self.map[(x, y)] =  val

    def expand(self, factor: int):
        extra = factor - 1
        x = 0
        while x < max([pos[0] for pos in self.map.keys()]):
            any_in_col = len([pos for pos in self.map.keys() if pos[0] == x]) > 0
            x += 1
            if any_in_col:
                continue

            right_galaxies = [pos for pos in self.map.keys() if pos[0] >= x]
            for galaxy in right_galaxies:
                new_pos = (galaxy[0] + extra, galaxy[1])
                self.map[new_pos] = self.map[galaxy]
                del self.map[galaxy]

            x += extra

        y = 0
        while y < max([pos[1] for pos in self.map.keys()]):
            any_in_row = len([pos for pos in self.map.keys() if pos[1] == y]) > 0
            y += 1
            if any_in_row:
                continue

            lower_galaxies = [pos for pos in self.map.keys() if pos[1] >= y]
            for galaxy in lower_galaxies:
                new_pos = (galaxy[0], galaxy[1] + extra)
                self.map[new_pos] = self.map[galaxy]
                del self.map[galaxy]

            y += extra


    def solve(self):
        start_time = time()

        self.parse_map()
        self.expand(2)

        part1 = 0
        for pair in combinations(self.map, 2):
            part1 += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])

        self.parse_map()
        self.expand(1_000_000)

        part2 = 0
        for pair in combinations(self.map, 2):
            part2 += abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])

        end_time = time()
        seconds_elapsed = end_time - start_time

        self.parse_map()
        self.image_map(self.map, {'#': (255, 255, 255)}, scale=5).save(self.visual_path('galaxies.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
