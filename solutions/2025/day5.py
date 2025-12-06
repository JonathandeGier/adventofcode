from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "Cafeteria"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        _ranges, ingredients = self.input.split('\n\n')

        ranges = []
        for _range in _ranges.splitlines():
            _min, _max = _range.split('-')
            _min, _max = int(_min), int(_max)

            # Make sure the ranges do not overlap
            overlaps = [r for r in ranges if _min <= r[1] and _max >= r[0]]
            for overlap in overlaps:
                ranges.remove(overlap)
                _min = min(_min, overlap[0])
                _max = max(_max, overlap[1])

            ranges.append((_min, _max))

        ingredients = [int(x) for x in ingredients.splitlines()]
        
        # Part 1
        part1 = 0
        for ingrediant in ingredients:
            fresh = False
            for _range in ranges:
                if ingrediant >= _range[0] and ingrediant <= _range[1]:
                    fresh = True
                    break

            if fresh:
                part1 += 1

        # Part 2
        part2 = 0
        for _range in ranges:
            part2 += _range[1] - _range[0] + 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
