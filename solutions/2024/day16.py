from Table import Table
from time import time
import heapq

TURN_AROUND = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
}

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Reindeer Maze"
        self.input = self.getInput(self.day)

        self.map = {}
        self.start = None
        self.end = None

    def parse_map(self):
        self.map = {}
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

    def solve(self):
        start_time = time()

        self.parse_map()

        queue = []
        visited = {}
        lowest_cost = None
        paths = []
        i = 0
        heapq.heappush(queue, (0, self.start, 'E', [self.start]))
        while len(queue) > 0:
            cost, pos, facing, path = heapq.heappop(queue)
            i += 1

            if pos == self.end:
                if lowest_cost == None or cost == lowest_cost:
                    lowest_cost = cost
                    part1 = lowest_cost
                    paths.append(path)
                else:
                    break

            if (pos, facing) in visited and visited[(pos, facing)] < cost:
                continue

            visited[(pos, facing)] = cost

            for dir, next_facing in {(1, 0): 'E', (0, 1): 'S', (-1, 0): 'W', (0, -1): 'N'}.items():
                next_pos = (pos[0] + dir[0], pos[1] + dir[1])

                if next_pos not in self.map:
                    continue

                if self.map[next_pos] == '#':
                    continue

                if next_facing == TURN_AROUND[facing]:
                    continue

                if next_facing == facing:
                    new_cost = cost + 1
                else:
                    new_cost = cost + 1001

                if (next_pos, next_facing) in visited and visited[(next_pos, next_facing)] < new_cost:
                    continue

                new_path = path.copy()
                new_path.append(next_pos)

                heapq.heappush(queue, (new_cost, next_pos, next_facing, new_path))

        locations = set()
        for path in paths:
            for pos in path:
                locations.add(pos)

        part1 = lowest_cost
        part2 = len(locations)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
