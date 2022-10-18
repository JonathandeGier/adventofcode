from Table import Table
from time import time

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Chronal Charge"
        self.input = int(self.getInput(self.day))

    def solve(self):
        start_time = time()

        grid = []
        for y in range(1, 301):
            row = []
            for x in range(1, 301):
                rack_id = x + 10
                power = rack_id * y
                power += self.input
                power = power * rack_id

                if len(str(power)) < 3:
                    power = 0
                else:
                    power = int(str(power)[-3])

                power -= 5

                row.append(power)
            grid.append(row)

        max_power = 0
        max_x = 0
        max_y = 0
        for x in range(0, 298):
            for y in range(0, 298):
                total_power = sum([sum(grid[_y][x:x+3]) for _y in range(y, y+3)])

                if total_power > max_power:
                    max_power = total_power
                    max_x = x + 1
                    max_y = y + 1


        part1 = str(max_x) + ',' + str(max_y)
        self.printRow((self.day, self.title, part1, '', ''), end="\r")

        max_power = 0
        max_x = 0
        max_y = 0
        max_size = 0
        for size in range(1, 30):
            self.printRow((self.day, self.title, part1, str(max_x) + ',' + str(max_y) + ',' + str(max_size) + ' (' + str(size) + ')', ''), end="\r")
            for x in range(0, 301 - size):
                for y in range(0, 301 - size):
                    total_power = total_power = sum([sum(grid[_y][x:x+size]) for _y in range(y, y+size)])

                    if total_power > max_power:
                        max_power = total_power
                        max_x = x + 1
                        max_y = y + 1
                        max_size = size

        part2 = str(max_x) + ',' + str(max_y) + ',' + str(max_size)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
