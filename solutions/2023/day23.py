from Table import Table
from time import time
import heapq
from collections import deque
from collections import defaultdict

PATH = '.'
FOREST = '#'

ILLEGAL_DIRECTION = {
    (0, 1):  '^',
    (1, 0):  '<',
    (0, -1): 'v',
    (-1, 0): '>',
}

LEGAL_DIRECTION = {
    (0, 1):  'v',
    (1, 0):  '>',
    (0, -1): '^',
    (-1, 0): '<',
}

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position: tuple=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "A Long Walk"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0

        self.start = None
        self.end = None

        self.vertexes = set()
        self.edges = {}

    def parse_map(self):
        # parse map to dictionary
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = val
        self.max_x = x
        self.max_y = y

        # search the start and end positions
        self.start = [pos for pos in self.map if pos[1] == 0 and self.map[pos] == PATH][0]
        self.end = [pos for pos in self.map if pos[1] == self.max_y and self.map[pos] == PATH][0]

        # mark the positions of all junctions in the map
        self.vertexes = set()
        self.vertexes.add(self.start)
        self.vertexes.add(self.end)
        for position in self.map:
            if self.map[position] == FOREST:
                continue

            neighbors = 0
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_position = (position[0] + direction[0], position[1] + direction[1])
                if new_position in self.map and self.map[new_position] != FOREST:
                    neighbors += 1
            
            if neighbors > 2:
                self.vertexes.add(position)

        # calculate the between vertexes (edges)
        self.edges = {}
        for vertex in self.vertexes:
            self.edges[vertex] = []
            queue = deque([(vertex, 0, None)])
            visited = set()
            while queue:
                position, length, allowed = queue.popleft()

                if position in visited:
                    continue

                visited.add(position)

                if position in self.vertexes and position != vertex:
                    assert allowed is not None, f'{vertex} to {position}'
                    self.edges[vertex].append((position, length, allowed))
                    continue

                for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_position = (position[0] + direction[0], position[1] + direction[1])

                    if new_position not in self.map or self.map[new_position] == FOREST:
                        continue

                    new_allowed = allowed
                    if self.map[new_position] in LEGAL_DIRECTION.values():
                        new_allowed = self.map[new_position] == LEGAL_DIRECTION[direction]

                    queue.append((new_position, length + 1, new_allowed))


    def hike_path(self, start: tuple, end: tuple, part1: bool = True):
        max_length = 0
        visited = defaultdict(lambda: False)

        def depth_first_search(position, length):
            nonlocal max_length

            if visited[position]:
                return
            visited[position] = True

            if position == end:
                max_length = max(max_length, length)

            for new_positions, distance, allowed in self.edges[position]:
                if part1 and not allowed:
                    continue

                depth_first_search(new_positions, length + distance)

            visited[position] = False

        depth_first_search(start, 0)

        return max_length
        

    def solve(self):
        start_time = time()

        self.parse_map()

        colors = {
            FOREST: (20, 150, 0), 
            PATH: (150, 90, 0),
            '^': (0, 200, 200),
            'v': (0, 200, 200),
            '<': (0, 200, 200),
            '>': (0, 200, 200),
        }
        self.image_map(self.map, colors, scale=5).save(self.visual_path('map.png'))

        part1 = self.hike_path(self.start, self.end, True)
        part2 = self.hike_path(self.start, self.end, False)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
