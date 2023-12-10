from Table import Table
from time import time

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Mirage Maintenance"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        readings = []
        for line in self.input.splitlines():
            differences = []
            differences.append([int(val) for val in line.split()])

            while True:
                last = differences[-1]
                diff = []
                for i in range(len(last) - 1):
                    diff.append(last[i + 1] - last[i])

                differences.append(diff)
                if all([val == 0 for val in diff]):
                    break

            readings.append(differences)


        part1 = 0
        part2 = 0
        for reading in readings:
            val1 = 0
            val2 = 0
            for i in range(len(reading) - 2, -1, -1):
                val1 = reading[i][-1] + val1
                val2 = reading[i][0] - val2

            part1 += val1
            part2 += val2

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
