from Table import Table
from time import time
from collections import deque

COLORS = {
    'A': (96,68,57),
    'B': (158,154,117),
    'C': (28,34,46),
    'D': (65,83,59),
    'E': (85,72,64),

    'F': (43,49,10),
    'G': (75,83,32),
    'H': (106,115,55),
    'I': (146,154,104),
    'J': (169,175,139),

    'K': (230,229,202),
    'L': (211,209,170),
    'M': (189,185,136),
    'N': (169,165,108),
    'O': (118,116,66),

    'P': (198,214,204),
    'Q': (124,152,129),
    'R': (78,107,77),
    'S': (46,64,40),
    'T': (38,47,27),

    'U': (31,55,47),
    'V': (47,60,40),
    'W': (56,59,38),
    'X': (61,58,36),
    'Y': (69,57,35),

    'Z': (96,68,57),
}

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Garden Groups"
        self.input = self.getInput(self.day)

        self.map = {}

    def parse_map(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[x, y] = val
        

    def solve(self):
        start_time = time()

        self.parse_map()

        part1 = 0
        part2 = 0
        visited = set()
        for pos in self.map:
            if pos in visited:
                continue

            region_visited = set()
            region_area = 0
            region_perimeter = 0
            perimeter_segments = {
                (0, 1): [], 
                (1, 0): [], 
                (0, -1): [], 
                (-1, 0): [],
            }
            queue = deque([pos])
            while len(queue) > 0:
                pos = queue.popleft()

                if pos in region_visited:
                    continue

                region_visited.add(pos)
                visited.add(pos)

                region_area += 1
                for dir in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
                    if new_pos not in self.map:
                        region_perimeter += 1
                        perimeter_segments[dir].append(new_pos)
                        continue

                    if self.map[new_pos] != self.map[pos]:
                        region_perimeter += 1
                        perimeter_segments[dir].append(new_pos)
                        continue

                    if new_pos in region_visited:
                        continue

                    queue.append(new_pos)
            
            sides = 0
            for dir, segments in perimeter_segments.items():
                edge = 1 if dir[0] == 0 else 0
                val = 0 if dir[0] == 0 else 1
                
                sides += 1
                segments.sort(key=lambda pos: (pos[edge], pos[val]))
                for i in range(1, len(segments)):
                    if segments[i][edge] != segments[i-1][edge]:
                        sides += 1
                        continue

                    if abs(segments[i][val] - segments[i-1][val]) != 1:
                        sides += 1

            part1 += region_area * region_perimeter
            part2 += region_area * sides


        self.image_map(self.map, COLORS, scale=10).save(self.visual_path('field.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
