from Table import Table
from time import time

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "I Was Told There Would Be No Math"
        self.input = Table.getInput(self.day)

    def get_lines(self):
        lines = self.input.splitlines()
        data = []
        for line in lines:
            row = []
            for length in line.split("x"):
                row.append(int(length))
            row.sort()
            data.append(row)

        return data

    def solve(self):
        start_time = time()

        totalArea = 0
        totalRibbon = 0
        for present in self.get_lines():
            area = (2 * present[0] * present[1]) + (2 * present[1] * present[2]) + (2 * present[0] * present[2]) + (present[0] * present[1])
            totalArea += area

            ribbon = (present[0] + present[0] + present[1] + present[1]) + (present[0] * present[1] * present[2])
            totalRibbon += ribbon

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, totalArea, totalRibbon, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
