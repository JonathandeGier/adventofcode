from Table import Table
from time import time
from collections import Counter

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Historian Hysteria"
        self.input = self.getInput(self.day)

    def parse_lists(self):
        list1, list2 = [], []
        for line in self.input.splitlines():
            left, right = line.split('   ')
            list1.append(int(left))
            list2.append(int(right))
        
        return list1, list2

    def solve(self):
        start_time = time()

        list1, list2 = self.parse_lists()
        assert len(list1) == len(list2)
        
        list1.sort()
        list2.sort()

        part1 = 0
        for i, val in enumerate(list1):
            val2 = list2[i]

            part1 += abs(val - val2)

        count = Counter(list2)
        part2 = 0
        for val in list1:
            if val in count:
                part2 += val * count.get(val)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
