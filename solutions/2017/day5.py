from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "A Maze of Twisty Trampolines, All Alike"
        self.input = self.getInput(self.day)

    def get_list(self):
        return [int(val) for val in self.input.splitlines()]

    def solve(self):
        start_time = time()

        jumps = self.get_list()

        i = 0
        steps = 0
        while i >= 0 and i < len(jumps):
            jump = jumps[i]
            jumps[i] += 1
            i += jump
            steps += 1

        part1 = steps

        jumps = self.get_list()

        i = 0
        steps = 0
        while i >= 0 and i < len(jumps):
            jump = jumps[i]
            if jump >= 3:
                jumps[i] -= 1
            else:
                jumps[i] += 1
            i += jump
            steps += 1

        # 442 < x < ...
        part2 = steps

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
