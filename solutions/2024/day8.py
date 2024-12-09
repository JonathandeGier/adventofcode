from Table import Table
from time import time
from itertools import combinations

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Resonant Collinearity"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0

    def antinodes(self, a: tuple, b: tuple):
        diff_x_a = a[0] - b[0]
        diff_y_a = a[1] - b[1]
        diff_x_b = b[0] - a[0]
        diff_y_b = b[1] - a[1]

        anti_a = (a[0] + diff_x_a, a[1] + diff_y_a)
        anti_b = (b[0] + diff_x_b, b[1] + diff_y_b)

        antinodes = []
        if anti_a[0] >= 0 and anti_a[0] <= self.max_x and anti_a[1] >= 0 and anti_a[1] <= self.max_y:
            antinodes.append(anti_a)
        if anti_b[0] >= 0 and anti_b[0] <= self.max_x and anti_b[1] >= 0 and anti_b[1] <= self.max_y:
            antinodes.append(anti_b)

        return antinodes
    
    def harmonic_antinodes(self, a: tuple, b: tuple):
        diff_x_a = a[0] - b[0]
        diff_y_a = a[1] - b[1]
        diff_x_b = b[0] - a[0]
        diff_y_b = b[1] - a[1]

        antinodes = [a, b]

        node = (a[0] + diff_x_a, a[1] + diff_y_a)
        while self.in_map(node):
            antinodes.append(node)
            node = (node[0] + diff_x_a, node[1] + diff_y_a)

        node = (b[0] + diff_x_b, b[1] + diff_y_b)
        while self.in_map(node):
            antinodes.append(node)
            node = (node[0] + diff_x_b, node[1] + diff_y_b)

        return antinodes

    def in_map(self, pos: tuple) -> bool:
        return pos[0] >= 0 and pos[0] <= self.max_x and pos[1] >= 0 and pos[1] <= self.max_y
    
    def parse_map(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val != '.':
                    self.map[x, y] = val

                self.max_x = max(x, self.max_x)
            self.max_y = max(y, self.max_y)

    def solve(self):
        start_time = time()

        self.parse_map()

        frequencies = set([val for val in self.map.values()])
        antinodes = set()
        harmonic_antinodes = set()
        for frequency in frequencies:
            positions = [entry[0] for entry in self.map.items() if entry[1] == frequency]
            for pair in combinations(positions, 2):
                # data = {}
                # for pos in pair:
                #     print(pos)
                #     data[pos] = 'A'
                # for pos in self.harmonic_antinodes(pair[0], pair[1]):
                #     print(pos)
                #     # if pos[0] >= 0 and pos[0] <= max_x and pos[1] >= 0 and pos[1] <= max_y:
                #     data[pos] = '#'

                # self.image_map(data, {'A': (255, 255, 255), '#': (150, 150, 150)}, (0, self.max_x, 0, self.max_y), scale=10).save(self.visual_path('test.png'))
                # exit()
                for antinode in self.antinodes(pair[0], pair[1]):
                    antinodes.add(antinode)

                for antinode in self.harmonic_antinodes(pair[0], pair[1]):
                    harmonic_antinodes.add(antinode)

        part1 = len(antinodes)

        # 853 < x < ...
        part2 = len(harmonic_antinodes)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
