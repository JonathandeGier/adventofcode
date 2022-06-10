from functools import reduce
from hashlib import new

from Table import Table
from time import time

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Disk Defragmentation"
        self.input = self.getInput(self.day).strip()

    def knot_hash(self, string):
        input_lengths = [ord(char) for char in string]
        input_lengths += [17, 31, 73, 47, 23]

        array = list(range(256))
        current_position = 0
        skip_size = 0

        for _ in range(64):
            array, current_position, skip_size = self.round(array, current_position, skip_size, input_lengths)

        dence_hash = []
        for i in range(0, 256, 16):
            dence_hash.append(reduce(lambda a, b: a ^ b, array[i:i + 16]))

        return [int(binval) for binval in ''.join(["{:08d}".format(int(bin(val)[2:])) for val in dence_hash])]

    def round(self, array: list, current_position: int, skip_size: int, lengths: list) -> tuple:
        for length in lengths:
            selected_sequence = []
            for i in range(length):
                selected_sequence.append(array[(current_position + i) % len(array)])

            selected_sequence = selected_sequence[::-1]

            for i in range(length):
                array[(current_position + i) % len(array)] = selected_sequence[i]

            current_position = (current_position + length + skip_size) % len(array)

            skip_size += 1

        return array, current_position, skip_size

    def get_grid(self):
        key = self.input
        grid = []
        for i in range(128):
            row_key = key + '-' + str(i)
            grid.append(self.knot_hash(row_key))

        return grid

    def solve(self):
        start_time = time()

        grid = self.get_grid()

        part1 = sum([sum(row) for row in grid])

        spots_to_group = set()  # set of coordinates, (row, column)
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 1:
                    spots_to_group.add((i, j))

        groups = []
        while len(spots_to_group) > 0:
            spot = spots_to_group.pop()
            group = []

            visited = set()
            queue = []
            queue.append(spot)
            while len(queue) > 0:
                spot = queue.pop()

                if spot in visited:
                    continue

                visited.add(spot)
                group.append(spot)

                if spot in spots_to_group:
                    spots_to_group.remove(spot)

                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_position = (spot[0] + direction[0], spot[1] + direction[1])

                    # outside grid
                    if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= 128 or new_position[1] >= 128:
                        continue

                    # spot is not used
                    if grid[new_position[0]][new_position[1]] != 1:
                        continue

                    # is already found in this group
                    if new_position in visited:
                        continue

                    queue.append(new_position)

            groups.append(groups)


        part2 = len(groups)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
