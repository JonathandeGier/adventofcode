import tarfile
from Table import Table
from time import time

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Chocolate Charts"
        self.input = int(self.getInput(self.day))

    def make_recipes(self):
        scores = [3, 7]
        elf1 = 0
        elf2 = 1

        target = self.input

        while len(scores) < target + 12:
            new_score = str(scores[elf1] + scores[elf2])
            for char in new_score:
                scores.append(int(char))

            elf1 = (elf1 + scores[elf1] + 1) % len(scores)
            elf2 = (elf2 + scores[elf2] + 1) % len(scores)

        return ''.join([str(score) for score in scores[target:target+10]])

    def make_backwards(self):
        scores = [3, 7]
        elf1 = 0
        elf2 = 1

        target = tuple([int(val) for val in str(self.input)])

        while True:
            new_score = str(scores[elf1] + scores[elf2])
            for char in new_score:
                scores.append(int(char))

            elf1 = (elf1 + scores[elf1] + 1) % len(scores)
            elf2 = (elf2 + scores[elf2] + 1) % len(scores)

            if len(scores) < len(target):
                continue

            if tuple(scores[-len(target):]) == target:
                return len(scores[:-len(target)])
            elif tuple(scores[-len(target) - 1:-1]) == target:
                return len(scores[:-len(target)-1])


    def solve(self):
        start_time = time()

        part1 = self.make_recipes()
        part2 = self.make_backwards()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
