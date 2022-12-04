from Table import Table
from time import time

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Camp Cleanup"
        self.input = self.getInput(self.day)

    def get_section_pairs(self):
        pairs = []
        for line in self.input.splitlines():
            elf1, elf2 = line.split(',')
            pairs.append((tuple([int(val) for val in elf1.split('-')]), tuple([int(val) for val in elf2.split('-')])))

        return pairs

    def solve(self):
        start_time = time()

        pairs = self.get_section_pairs()

        part1 = 0
        for pair in pairs:
            if (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]) or (pair[1][0] <= pair[0][0] and pair[1][1] >= pair[0][1]):
                part1 += 1

        part2 = 0
        for pair in pairs:
            if pair[0][0] <= pair[1][1] and pair[0][1] >= pair[1][0]:
                part2 += 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
