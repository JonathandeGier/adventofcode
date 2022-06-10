import heapq
from math import sqrt
from typing import Counter
from Table import Table
from time import time

# shift all hexes to make as square grid

#      \ n  /
#    nw +--+ ne
#      /    \
#    -+      +-
#      \    /
#    sw +--+ se
#      / s  \
# 
#        |
#        V
# 
#    \
# nw  +
#    / \ n  /	
# --+   +--+   +--
#    \ /    \ /
# sw  +      +  ne
#    / \    / \
# --+   +--+   +--
#    \ / s  \ /
#     +      +  se
#      \    / \

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Hex Ed"
        self.input = self.getInput(self.day)[:-1]

    def get_moves(self):
        return [move for move in self.input.split(',')]

    def astar(self, start, end):
        start_node = Node(None, start)
        end_node = Node(None, end)

        queue = []
        visited = {}

        heapq.heappush(queue, (0, start, start_node))

        while len(queue) > 0:

            # get node with lowest cost
            length, _, current_node = heapq.heappop(queue)

            if current_node.position in visited:
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
            for position_difference in [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]: # north, north-east, south-east, south, south-west, north-west
                new_position = (current_node.position[0] + position_difference[0], current_node.position[1] + position_difference[1])

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

        moves = self.get_moves()
        max_distance = 0
        position = (0, 0)
        for i, move in enumerate(moves):
            if move == 'n':
                position = (position[0], position[1] + 1)
            elif move == 'ne':
                position = (position[0] + 1, position[1])
            elif move == 'se':
                position = (position[0] + 1, position[1] - 1)
            elif move == 's':
                position = (position[0], position[1] - 1)
            elif move == 'sw':
                position = (position[0] - 1, position[1])
            elif move == 'nw':
                position = (position[0] - 1, position[1] + 1)
            else:
                assert False, 'Unknown move: ' + move

            distance = len(self.astar((0, 0), position)) - 1
            max_distance = max(max_distance, distance)

            per = round((i / len(moves)) * 100, 1)
            percentage = str(per) + ' %'
            self.printRow((self.day, self.title, percentage, percentage, ''), end="\r")
        
        part1 = distance
        part2 = max_distance

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
