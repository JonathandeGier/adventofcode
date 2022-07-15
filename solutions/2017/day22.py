from collections import defaultdict
from turtle import position

from jsii import enum
from Table import Table
from time import time

class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Sporifica Virus"
        self.input = self.getInput(self.day)

    def get_grid(self):
        grid = defaultdict(lambda: False)
        lines = self.input.splitlines()
        widht = len(lines[0])
        height = len(lines)

        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                if val == '.':
                    value = False
                elif val == '#':
                    value = True
                else:
                    assert False

                grid[(col - (widht // 2), (height // 2) - row)] = value
            
        return grid

    def get_state_grid(self):
        grid = defaultdict(lambda: 'clean')
        lines = self.input.splitlines()
        widht = len(lines[0])
        height = len(lines)

        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                if val == '.':
                    value = 'clean'
                elif val == '#':
                    value = 'infected'
                else:
                    assert False

                grid[(col - (widht // 2), (height // 2) - row)] = value
            
        return grid

    def solve(self):
        start_time = time()

        grid = self.get_grid()

        right = {
            'up': 'right',
            'down': 'left',
            'left': 'up',
            'right': 'down',
        }

        left = {
            'up': 'left',
            'down': 'right',
            'left': 'down',
            'right': 'up',
        }

        current_position = (0, 0)
        direction = 'up'
        infect_count = 0

        for _ in range(10_000):
            if grid[current_position]:
                direction = right[direction]
            else:
                direction = left[direction]

            if grid[current_position]:
                grid[current_position] = False
            else:
                grid[current_position] = True
                infect_count += 1

            if direction == 'up':
                new_position = (current_position[0], current_position[1] + 1)
            elif direction == 'down':
                new_position = (current_position[0], current_position[1] - 1)
            elif direction == 'left':
                new_position = (current_position[0] - 1, current_position[1])
            elif direction == 'right':
                new_position = (current_position[0] + 1, current_position[1])
            else:
                assert False

            current_position = new_position

        part1 = infect_count

        reverse = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left',
        }

        grid = self.get_state_grid()

        current_position = (0, 0)
        direction = 'up'
        infect_count = 0

        for i in range(10_000_000):
            if i % 200_000 == 0:
                self.printRow((self.day, self.title, part1, str(round((i / 10_000_000) * 100, 2)) + ' %', ''), end="\r")

            if grid[current_position] == 'clean':
                direction = left[direction]
            elif grid[current_position] == 'infected':
                direction = right[direction]
            elif grid[current_position] == 'flagged':
                direction = reverse[direction]

            if grid[current_position] == 'clean':
                grid[current_position] = 'weakened'
            elif grid[current_position] == 'weakened':
                grid[current_position] = 'infected'
                infect_count += 1
            elif grid[current_position] == 'infected':
                grid[current_position] = 'flagged'
            elif grid[current_position] == 'flagged':
                grid[current_position] = 'clean'

            if direction == 'up':
                new_position = (current_position[0], current_position[1] + 1)
            elif direction == 'down':
                new_position = (current_position[0], current_position[1] - 1)
            elif direction == 'left':
                new_position = (current_position[0] - 1, current_position[1])
            elif direction == 'right':
                new_position = (current_position[0] + 1, current_position[1])
            else:
                assert False

            current_position = new_position

        part2 = infect_count

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
