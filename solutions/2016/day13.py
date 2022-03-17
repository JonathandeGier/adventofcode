from turtle import position
from typing import Counter

from matplotlib.pyplot import grid
from Table import Table
from time import time

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


class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "A Maze of Twisty Little Cubicles"
        self.input = int(self.getInput(self.day).strip())
        self.grid = {}

    def is_walkable(self, pos: tuple) -> bool:
        if pos not in self.grid:
            x = pos[0]
            y = pos[1]
            val = (x*x) + (x*3) + (2*x*y) + y + (y*y) + self.input

            count = Counter(bin(val))
            self.grid[(x,y)] = count['1'] % 2 == 0 # True is open space, false is cubicale

        return self.grid[pos]

    def astar(self, start, end, max_steps = None):
        start_node = Node(None, start)
        end_node = Node(None, end)

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:

            # get node with lowest cost
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

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
            for position_difference in [(0,-1), (1,0), (0,1), (-1,0)]: # up, right, down, left (north, east, south, west)
                new_position = (current_node.position[0] + position_difference[0], current_node.position[1] + position_difference[1])
                
                # make sure the new position is not outside the grid
                if new_position[0] < 0 or new_position[1] < 0:
                    continue

                # make sure the new position is walkable
                if not self.is_walkable(new_position):
                    continue

                new_node = Node(current_node, new_position)
                directions.append(new_node)

            for direction in directions:
                if direction in closed_list:
                    continue

                direction.g = current_node.g + 1
                direction.h = ((direction.position[0] - end_node.position[0]) ** 2) + ((direction.position[1] - end_node.position[1]) ** 2)
                direction.f = direction.g + direction.h

                if max_steps is not None and direction.g > max_steps:
                    continue

                for open_node in open_list:
                    if direction == open_node and direction.g > open_node.g:
                        continue

                open_list.append(direction)

        # No path found
        return False

            

    def solve(self):
        start_time = time()

        start = (1,1)
        end = (31,39)

        path = self.astar(start, end)
        part1 = len(path) - 1

        locations = []
        for x in range(30):
            for y in range(30):
                location = (x,y)
                if self.is_walkable(location) and self.astar(start, location, 50) is not False:
                    locations.append(location)

        part2 = len(locations)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
