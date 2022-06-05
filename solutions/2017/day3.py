from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Spiral Memory"
        self.input = int(self.getInput(self.day))

    def next(self, current, grid):
        new_positions = []
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_positions.append((current[0] + direction[0], current[1] + direction[1]))

        if new_positions[0] not in grid and new_positions[1] not in grid and new_positions[2] not in grid and new_positions[3] not in grid:
            return new_positions[1]
        elif new_positions[0] in grid and new_positions[1] not in grid:
            return new_positions[1]
        elif new_positions[1] in grid and new_positions[2] not in grid:
            return new_positions[2]
        elif new_positions[2] in grid and new_positions[3] not in grid:
            return new_positions[3]
        elif new_positions[0] not in grid and new_positions[3] in grid:
            return new_positions[0]
        else:
            print(new_positions, grid)
            assert False
        

    def solve(self):
        start_time = time()

        center = (0, 0)
        current = 1
        current_pos = center
        grid = {center: current}

        while current < self.input:
            current += 1
            current_pos = self.next(current_pos, grid)
            grid[current_pos] = current


        part1 = sum([abs(val) for val in current_pos])
        
        # Part 2
        center = (0, 0)
        value = 1
        current_pos = center
        grid = {center: value}

        while value < self.input:
            current_pos = self.next(current_pos, grid)

            value_positions = []
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0),  (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                value_positions.append((current_pos[0] + direction[0], current_pos[1] + direction[1]))

            value = sum([grid[value_position] for value_position in value_positions if value_position in grid])

            grid[current_pos] = value
        
        part2 = value

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
