from re import X
from xml.dom.NodeFilter import NodeFilter
from xml.dom.minicompat import NodeList
from xmlrpc.server import SimpleXMLRPCDispatcher
from matplotlib.style import use
from Table import Table
from time import time

class Node:
    def __init__(self, x: int, y: int, size: int, used: int, available: int):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.available = available

    def __eq__(self, __o: object) -> bool:
        return type(__o) == Node and __o.x == self.x and __o.y == self.y

class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Grid Computing"
        self.input = self.getInput(self.day)
        self.tile_grid = None

    def get_grid(self) -> list:
        grid = []
        row = []
        for line in self.input.splitlines()[2:]:
            segments = line.split(' ')
            
            location = segments[0].split('-')
            x = int(location[1][1:])
            y = int(location[2][1:])

            size = None
            used = None
            available = None
            for item in segments[1:]:
                if item != '':
                    if size == None:
                        size = int(item[:-1])
                    elif used == None:
                        used = int(item[:-1])
                    elif available == None:
                        available = int(item[:-1])
                        break
                    else:
                        assert False

            row.append(Node(x, y, size, used, available))

            if y == 30:
                grid.append(row)
                row = []
        return grid

    def get_tile_grid(self, grid):
        tile_grid = []
        
        for row in grid:
            tile_row = []
            for node in row:
                if node.x == 31 and node.y == 0:
                    tile_row.append('G')
                elif node.x == 0 and node.y == 0:
                    tile_row.append('*')
                elif node.size > 100:
                    tile_row.append('#')
                elif node.used == 0:
                    tile_row.append('_')
                else:
                    tile_row.append('.')
            tile_grid.append(tile_row)

        return tile_grid


    def flatten(self, array: list) -> list:
        newArray = []
        for item in array:
            for subItem in item:
                newArray.append(subItem)
        return newArray


    def print_grid(self) -> None:
        for row in self.tile_grid:
            for node in row:
                print(node, end=' ')
            print('')


    def solve(self):
        start_time = time()

        grid = self.get_grid()
        nodeList = self.flatten(grid)

        pairs = 0
        for startNode in nodeList:
            for endNode in nodeList:
                if startNode.used != 0 and startNode != endNode and startNode.used <= endNode.available:
                    pairs += 1

        part1 = pairs

        # Part 2 printed out and solved manually
        part2 = "179 *"

        self.tile_grid = self.get_tile_grid(grid)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
    day.print_grid()
    print("")
