from Table import Table
from time import time

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Tuning Trouble"
        self.input = self.getInput(self.day).strip()

    def solve(self):
        start_time = time()

        part1 = 0
        for i in range(0, len(self.input)):
            marker = self.input[i:i+4]
            marker_set = set(marker)

            if len(marker_set) == 4:
                part1 = i + 4
                break

        part2 = 0
        for i in range(0, len(self.input)):
            marker = self.input[i:i+14]
            marker_set = set(marker)

            if len(marker_set) == 14:
                part2 = i + 14
                break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
