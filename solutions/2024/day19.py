from Table import Table
from time import time

CACHE = {}

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Linen Layout"
        self.input = self.getInput(self.day)

        self.max_pattern_length = 0
    

    def possible_ways(self, design: str, patterns: set):
        if design in CACHE:
            return CACHE[design]
        
        options = 0
        if design in patterns:
            options += 1
        
        for length in range(1, self.max_pattern_length + 1):
            if length >= len(design):
                continue

            if design[:length] in patterns:
                options += self.possible_ways(design[length:], patterns)

        CACHE[design] = options

        return options
    

    def solve(self):
        start_time = time()

        patterns, designs = self.input.split('\n\n')
        patterns = set([pattern.strip() for pattern in patterns.split(',')])
        for pattern in patterns:
            self.max_pattern_length = max(self.max_pattern_length, len(pattern))

        part1 = 0
        part2 = 0
        for design in designs.splitlines():
            options = self.possible_ways(design, patterns)
            
            if options > 0:
                part1 += 1

            part2 += options


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
