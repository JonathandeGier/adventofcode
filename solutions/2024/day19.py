from Table import Table
from time import time

CACHE = {}

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = ""
        self.input = self.getInput(self.day)

    def possible(self, design: str, patterns: set, depth = 0) -> bool:
        if design in CACHE:
            return CACHE[design]

        if design in patterns:
            CACHE[design] = True
            return True

        # print(design, CACHE)
        possible = False
        for length in range(1, 11):
            if length >= len(design):
                continue

            seg = design[:length]
            rest = design[length:]
            if seg in patterns and self.possible(rest, patterns, depth + 1):
                possible = True
                break

        CACHE[design] = possible

        return possible

    def solve(self):
        start_time = time()

        patterns, designs = self.input.split('\n\n')
        patterns = set([pattern.strip() for pattern in patterns.split(',')])

        part1 = 0
        part2 = 0
        for design in designs.splitlines():
            print(design)
            if self.possible(design, patterns):
                part1 += 1


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
