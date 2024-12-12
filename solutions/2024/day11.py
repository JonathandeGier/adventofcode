from Table import Table
from time import time

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Plutonian Pebbles"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        stones = [int(x) for x in self.input.strip().split(' ')]
        counts = {}
        for stone in stones:
            if stone not in counts:
                counts[stone] = 0
            counts[stone] += 1

        p1_counts = None
        for i in range(75):
            if i == 25:
                p1_counts = counts

            new_counts = {}
            for stone, count in counts.items():
                if stone == 0:
                    if 1 not in new_counts:
                        new_counts[1] = 0
                    new_counts[1] += count
                elif len(str(stone)) % 2 == 0:
                    mid = len(str(stone)) // 2
                    new_stone_1 = int(str(stone)[0:mid])
                    new_stone_2 = int(str(stone)[mid:])

                    if new_stone_1 not in new_counts:
                        new_counts[new_stone_1] = 0
                    new_counts[new_stone_1] += count

                    if new_stone_2 not in new_counts:
                        new_counts[new_stone_2] = 0
                    new_counts[new_stone_2] += count
                else:
                    new_stone = stone * 2024
                    if new_stone not in new_counts:
                        new_counts[new_stone] = 0
                    new_counts[new_stone] += count
            counts = new_counts

        part1 = sum(count for count in p1_counts.values())
        part2 = sum(count for count in counts.values())

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
