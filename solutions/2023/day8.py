from Table import Table
from time import time
import math

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Haunted Wasteland"
        self.input = self.getInput(self.day)

        self.path = ''
        self.nodes = {}

    def parse_nodes(self):
        self.path, nodes = self.input.split('\n\n')
        
        self.nodes = {}
        for node in nodes.splitlines():
            src, target = node.split(' = ')
            left, right = target[1:-1].split(', ')
            self.nodes[src] = (left, right)

    def solve(self):
        start_time = time()

        self.parse_nodes()

        step = 0
        current = 'AAA'
        while True:
            dir = self.path[step % len(self.path)]
            step += 1

            if dir == 'L':
                current = self.nodes[current][0]
            elif dir == 'R':
                current = self.nodes[current][1]
            else:
                assert False, f'Unknown direction {dir}'

            if current == 'ZZZ':
                break

        part1 = step

        step = 0
        current_nodes = [node for node in self.nodes.keys() if node[2] == 'A']
        repeats = {}
        while True:
            dir = self.path[step % len(self.path)]
            step += 1

            for i, current in enumerate(current_nodes):
                if dir == 'L':
                    current_nodes[i] = self.nodes[current][0]
                elif dir == 'R':
                    current_nodes[i] = self.nodes[current][1]
                else:
                    assert False, f'Unknown direction {dir}'

                if current_nodes[i][2] == 'Z':
                    repeats[i] = step

            if len(repeats.keys()) == len(current_nodes):
                break

        part2 = math.lcm(*repeats.values())

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
