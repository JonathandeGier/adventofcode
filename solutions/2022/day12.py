from Table import Table
from time import time
import heapq
from PIL import Image

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

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Hill Climbing Algorithm"
        self.input = self.getInput(self.day)

        self.map = {}
        self.start = None
        self.end = None

        self.max_x = 0
        self.max_y = 0

    def load_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            self.max_y = max(self.max_y, y)
            for x, val in enumerate(line):
                self.max_x = max(self.max_x, x)
                if val == 'S':
                    self.map[x, y] = 1
                    self.start = (x, y)
                elif val == 'E':
                    self.map[x, y] = 26
                    self.end = (x, y)
                else:
                    self.map[x, y] = ord(val) - 96

    def astar(self, start: tuple, end: tuple):
        start_node = Node(None, start)
        end_node = Node(None, end)

        queue = []
        visited = {}

        heapq.heappush(queue, (0, start, start_node))

        while len(queue) > 0:

            # get node with lowest cost
            length, _, current_node = heapq.heappop(queue)

            if current_node.position in visited and visited[current_node.position] <= length:
                continue

            visited[current_node.position] = length

            # check if the current node is the end node and return the path if so
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            # generate next possible directions
            directions = []
            for position_difference in [(0, 1), (0, -1), (-1, 0), (1, 0)]: # up, down, left, right
                new_position = (current_node.position[0] + position_difference[0], current_node.position[1] + position_difference[1])

                if new_position not in self.map:
                    # print('not in map:', new_position)
                    continue

                if self.map[new_position] > self.map[current_node.position] + 1:
                    # print('to high:', self.map[new_position], self.map[current_node.position])
                    continue

                new_node = Node(current_node, new_position)
                directions.append(new_node)

            for direction in directions:

                direction.g = current_node.g + 1
                direction.h = ((direction.position[0] - end_node.position[0]) ** 2) + ((direction.position[1] - end_node.position[1]) ** 2)
                direction.f = direction.g + direction.h

                if direction.position not in visited or visited[direction.position] > direction.h:
                    heapq.heappush(queue, (direction.f, direction.position, direction))

        # No path found
        return False

    def solve(self):
        start_time = time()

        self.load_map()

        self.image().save(self.visual_path('map.png'))

        path = self.astar(self.start, self.end)
        part1 = len(path) - 1

        self.image(path).save(self.visual_path('map-part1.png'))

        # there are a lot of positions with value a
        # there is a "wall" of value b that we have to go through on x=1, since all values where x>1 are a or greater than b
        # to limit the search space, only select start positions on x=0
        possible_starts = [position for position in self.map.keys() if self.map[position] == 1 and position[0] == 0]
        min_distance = 1_000_000_000_000
        shortest_path = []
        for start in possible_starts:
            path = self.astar(start, self.end)
            if path == False:
                continue

            distance = len(path) - 1
            if distance < min_distance:
                min_distance = distance
                shortest_path = path

        part2 = min_distance

        self.image(shortest_path).save(self.visual_path('map-part2.png'))

        end_time = time()

        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, path: list = []):
        img = Image.new('RGB', (self.max_x + 1, self.max_y + 1), 'black')
        pixels = img.load()
        for location in self.map.keys():
            value = self.map[location] * 8
            pixels[location] = (value, value, value)

        for location in path:
            value = self.map[location] * 10
            pixels[location] = (value, value, value // 2)

        scale = 8
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
