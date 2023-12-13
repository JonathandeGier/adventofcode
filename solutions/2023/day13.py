from Table import Table
from time import time

class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Point of Incidence"
        self.input = self.getInput(self.day)

        self.patterns = []


    def parse_patterns(self):
        self.patterns = []
        for raw_pattern in self.input.split('\n\n'):
            pattern = {}
            for y, line in enumerate(raw_pattern.splitlines()):
                for x, val in enumerate(line):
                    pattern[(x, y)] = val

            self.patterns.append(pattern)


    def is_mirrored_on_row(self, pattern: dict, row: int) -> tuple[bool, bool]:
        max_col = max([pos[0] for pos in pattern])
        max_row = max([pos[1] for pos in pattern])
        smudge = False

        for y in range(row + 1, max_row + 1):
            mirr_y = row - (y - row - 1)
            if mirr_y < 0:
                break

            for x in range(max_col + 1):
                if pattern[(x, y)] != pattern[(x, mirr_y)]:
                    if not smudge:
                        smudge = True
                    else:
                        return (False, False)
                
        return (True, smudge)


    def is_mirrored_on_col(self, pattern: dict, col: int) -> tuple[bool, bool]:
        max_col = max([pos[0] for pos in pattern])
        max_row = max([pos[1] for pos in pattern])
        smudge = False

        for x in range(col + 1, max_col + 1):
            mirr_x = col - (x - col - 1)
            if mirr_x < 0:
                break

            for y in range(max_row + 1):
                if pattern[(x, y)] != pattern[(mirr_x, y)]:
                    if not smudge:
                        smudge = True
                    else:
                        return (False, False)
                
        return (True, smudge)


    def find_mirror(self, pattern: dict, allow_smudge: bool = False):
        max_x = max([pos[0] for pos in pattern])
        max_y = max([pos[1] for pos in pattern])

        for x in range(max_x):
            valid, smudge = self.is_mirrored_on_col(pattern, x)
            if valid and smudge == allow_smudge:
                return ('x', x)
            
        for y in range(max_y):
            valid, smudge = self.is_mirrored_on_row(pattern, y)
            if valid and smudge == allow_smudge:
                return ('y', y)

        return None


    def solve(self):
        start_time = time()

        self.parse_patterns()

        part1 = 0
        part2 = 0
        for pattern in self.patterns:
            reflection = self.find_mirror(pattern)
            smudge_reflection = self.find_mirror(pattern, True)

            if reflection[0] == 'x':
                part1 += reflection[1] + 1
            elif reflection[0] == 'y':
                part1 += (100 * (reflection[1] + 1))

            if smudge_reflection[0] == 'x':
                part2 += smudge_reflection[1] + 1
            elif smudge_reflection[0] == 'y':
                part2 += (100 * (smudge_reflection[1] + 1))


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
