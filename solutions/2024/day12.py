from Table import Table
from time import time
from collections import deque

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
            
            print(self.map[pos])
            sides = 0
            for dir, segments in perimeter_segments.items():
                edge = 1 if dir[0] == 0 else 0
                val = 0 if dir[0] == 0 else 1
                print(dir, segments)
                
                sides += 1
                segments.sort(key=lambda pos: pos[edge])
                print(dir,segments)
                for i in range(1, len(segments)):
                    if segments[i][edge] != segments[i-1][edge]:
                        sides += 1
                        continue

                    print(abs(segments[i][val] - segments[i-1][val]))
                    if abs(segments[i][val] - segments[i-1][val]) != 1:
                        pass
                    else:
                        sides += 1

            print(sides)
            exit()
            part1 += region_area * region_perimeter
            # print(self.map[pos], region_area, region_perimeter)


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
