from Table import Table
from time import time

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "Like a GIF For Your Yard"
        self.input = self.getInput(self.day)

    def get_lights(self):
        grid = []
        for line in self.input.splitlines():
            row = []
            for val in line:
                if val == "#":
                    row.append(True)
                else:
                    row.append(False)
            grid.append(row)

        return grid

    def animate(self, lights, iterations, p1 = True):
        for _ in range(iterations):
            new_lights = []
            for row, row_data in enumerate(lights):
                new_row = []
                for col, val in enumerate(row_data):

                    neighbours_on = 0
                    for diff in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                        r = row + diff[0]
                        c = col + diff[1]
                        if r < 0 or c < 0 or r == len(lights) or c == len(lights[0]):
                            continue

                        neighbours_on += lights[r][c]

                    if not p1 and ((row == 0 and col == 0) or (row == 0 and col == len(lights[0]) - 1) or (row == len(lights) - 1 and col == 0) or (row == len(lights) - 1 and col == len(lights[0]) - 1)):
                        new_row.append(True)
                    else:
                        if val:
                            if neighbours_on >= 2 and neighbours_on <= 3:
                                new_row.append(True)
                            else:
                                new_row.append(False)
                        else:
                            if neighbours_on == 3:
                                new_row.append(True)
                            else:
                                new_row.append(False)
                new_lights.append(new_row)
            lights = new_lights
        return lights

    def print_lights(lights):
        for row in lights:
            for val in row:
                if val:
                    print("#", end="", flush=True)
                else:
                    print(".", end="", flush=True)
            print("")


    def solve(self):
        start_time = time()

        lights = self.get_lights()

        lights = self.animate(lights, 100, True)
        part1 = sum([sum(row) for row in lights])

        lights = self.get_lights()

        lights[0][0] = True
        lights[0][len(lights[0])-1] = True
        lights[len(lights)-1][0] = True
        lights[len(lights)-1][len(lights[0])-1] = True

        lights = self.animate(lights, 100, False)
        part2 = sum([sum(row) for row in lights])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
