from Table import Table
from time import time

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Chronal Calibration"
        self.input = self.getInput(self.day)

    def get_changes(self):
        return [int(x) for x in self.input.splitlines()]

    def solve(self):
        start_time = time()

        changes = self.get_changes()

        part1 = sum(changes)

        seen = set()
        i = 0
        current = 0
        while current not in seen:
            seen.add(current)
            change = changes[i % len(changes)]

            current += change
            i += 1

        part2 = current

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
