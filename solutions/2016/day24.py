from collections import deque
import heapq
from itertools import product
import sys

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


class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Air Duct Spelunking"
        self.input = self.getInput(self.day)

        self.maze = {}
        self.max_x = 0
        self.max_y = 0

        self.points = {}

    def load_maze(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, char in enumerate(line):
                if char not in ['#', '.']:
                    self.points[char] = (x, y)
                    self.maze[(x, y)] = '.'
                else:
                    self.maze[(x, y)] = char

                self.max_x = max(self.max_x, x)
                self.max_y = max(self.max_y, y)
    
    def print_maze(self, highlight=None):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if highlight == (x, y):
                    print('O', end='')
                else:
                    print(self.maze[(x, y)], end='')
            print('')

    def astar(self, start, end):
        start_node = Node(None, start)
        end_node = Node(None, end)

        queue = []
        visited = set()

        heapq.heappush(queue, (0, start, start_node))

        while len(queue) > 0:

            # get node with lowest cost
            lll, _, current_node = heapq.heappop(queue)
            visited.add(current_node.position)

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
                
                # make sure the new position is not outside the maze
                if new_position[0] < 0 or new_position[1] < 0 or new_position[0] > self.max_x or new_position[1] > self.max_y:
                    continue

                # make sure the new position is walkable
                if self.maze[new_position] == '#':
                    continue

                # dont go back
                if current_node.parent is not None and current_node.parent.position == new_position:
                    continue

                new_node = Node(current_node, new_position)
                directions.append(new_node)

            for direction in directions:
                if direction.position in visited:
                    continue

                direction.g = current_node.g + 1
                direction.h = ((direction.position[0] - end_node.position[0]) ** 2) + ((direction.position[1] - end_node.position[1]) ** 2)
                direction.f = direction.g + (direction.h * (1 / direction.g))

                heapq.heappush(queue, (direction.f, direction.position, direction))

        # No path found
        return False

    def solve(self):
        start_time = time()

        self.load_maze()

        # precompute path lengths
        all_path_lengths = {}
        for path in product(['0', '1', '2', '3', '4', '5', '6', '7'], repeat=2):
            # dont go to where you already are
            if path[0] == path[1]:
                continue
            
            steps = len(self.astar(self.points[path[0]], self.points[path[1]])) - 1
            all_path_lengths[path] = steps

        # path algorithm doesnt return the shortest path, but is pretty close with some guess work
        path_lengths = {}
        for path in all_path_lengths:
            key = (min(path), max(path))
            if key not in path_lengths:
                path_lengths[key] = all_path_lengths[path]
            else:
                path_lengths[key] = min(path_lengths[key], all_path_lengths[path])

        # mini astar to find shortest path though all numbers
        current = '0'
        visited = ['0']
        steps = 0

        queue = []

        least_steps = None

        heapq.heappush(queue, (steps, visited, current))

        while len(queue) > 0:
            steps, visited, current = heapq.heappop(queue)

            if len(visited) == 8:
                least_steps = steps
                break

            options = set(('1', '2', '3', '4', '5', '6', '7')).difference(set(visited))
            
            for option in options:
                local_visited = visited.copy()
                local_visited.append(option)
                pathkey = (min(current, option), max(current, option))

                heapq.heappush(queue, (steps + path_lengths[pathkey], local_visited, option))

        part1 = least_steps
        
        # part 2
        current = '0'
        visited = []
        steps = 0

        queue = []

        least_steps = sys.maxsize

        heapq.heappush(queue, (steps, visited, current))

        while len(queue) > 0:
            steps, visited, current = heapq.heappop(queue)

            if len(visited) == 8:
                least_steps = min(least_steps, steps)
                

            nums = ('1', '2', '3', '4', '5', '6', '7')
            if len(visited) == 7:
                nums = ('1', '2', '3', '4', '5', '6', '7', '0')

            options = set(nums).difference(set(visited))
            
            for option in options:
                local_visited = visited.copy()
                local_visited.append(option)
                pathkey = (min(current, option), max(current, option))

                heapq.heappush(queue, (steps + path_lengths[pathkey], local_visited, option))

        end_time = time()
        seconds_elapsed = end_time - start_time

        part2 = least_steps

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
