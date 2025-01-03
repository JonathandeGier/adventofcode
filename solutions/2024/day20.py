from Table import Table
from time import time
from collections import deque


class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Race Condition"
        self.input = self.getInput(self.day)

        self.map = {}
        self.start = None
        self.end = None

    def parse_map(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == 'S':
                    self.start = (x, y)
                    self.map[x, y] = '.'
                elif val == 'E':
                    self.end = (x, y)
                    self.map[x, y] = '.'
                else:
                    self.map[x, y] = val

    def manhatten_points(self, pos, distance):
        points = []
        for dist in range(1, distance + 1):
            for offset in range(dist):
                invOffset = dist - offset
                points.append((pos[0] + offset, pos[1] + invOffset))
                points.append((pos[0] + invOffset,pos[1] - offset))
                points.append((pos[0] - offset, pos[1] - invOffset))
                points.append((pos[0] - invOffset, pos[1] + offset))
        return points
    
    def manhatten_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def solve_part(self, cost: dict, cheat_distance: int) -> int:
        cheats = set()
        answer = 0
        for cheat_start in cost.keys():
            cheat_ends = self.manhatten_points(cheat_start, cheat_distance)
            for cheat_end in cheat_ends:
                if cheat_end == cheat_start or cheat_end not in self.map or self.map[cheat_end] != '.':
                    continue

                if (cheat_start, cheat_end) in cheats:
                    continue
                cheats.add((cheat_start, cheat_end))

                save = cost[cheat_end] - cost[cheat_start] - self.manhatten_distance(cheat_start, cheat_end)
                if save >= 100:
                    answer += 1

        return answer

    def solve(self):
        start_time = time()

        self.parse_map()

        # Determine cost for each position
        cost = {}
        queue = deque([(self.start, 0)])
        while len(queue) > 0:
            pos, steps = queue.popleft()
            
            cost[pos] = steps
            if pos == self.end:
                break
                
            for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (pos[0] + dir[0], pos[1] + dir[1])
                if next_pos not in self.map:
                    continue
                    
                if self.map[next_pos] != '.':
                    continue
                    
                if next_pos in cost:
                    continue
                    
                queue.append((next_pos, steps+1))

        part1 = self.solve_part(cost, 2)
        part2 = self.solve_part(cost, 20)

        if __name__ == '__main__':
            self.image_map(self.map, {'#': (255, 255, 255)}, scale=7).save(self.visual_path('map.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
