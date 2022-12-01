from Table import Table
from time import time

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Calorie Counting"
        self.input = self.getInput(self.day)

    def get_elfs(self):
        elfs = []
        current_elf = []
        for line in self.input.splitlines():
            if line == "":
                elfs.append(current_elf)
                current_elf = []
                continue

            current_elf.append(int(line))

        return elfs

    def solve(self):
        start_time = time()

        elfs = self.get_elfs()

        sums = [sum(cals) for cals in elfs]
        part1 = max(sums)

        sorted_sums = sorted(sums, reverse=True)
        part2 = sum(sorted_sums[:3])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
