from Table import Table
from time import time
import re

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Mull It Over"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()
        
        matches = re.findall(r"(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don)\'t\(\)", self.input, )

        part1 = 0
        part2 = 0
        enabled = True
        for match in matches:
            if match[0] == 'mul':
                part1 += int(match[1]) * int(match[2])
                if enabled:
                    part2 += int(match[1]) * int(match[2])
            elif match[3] == 'do':
                enabled = True
            elif match[4] == 'don':
                enabled = False

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
