from Table import Table
from time import time

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Code Chronicle"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        keys = []
        locks = []
        for template in self.input.split('\n\n'):
            is_key = None
            parsed = []
            for y, line in enumerate(template.splitlines()):
                if y == 0:
                    is_key = True if '#' not in line else False
                    parsed = [0 for _ in line]

                for i, val in enumerate(line):
                    if is_key and val == '.':
                        parsed[i] = 5 - y
                    elif not is_key and val == '#':
                        parsed[i] = y

            if is_key:
                keys.append(tuple(parsed))
            else:
                locks.append(tuple(parsed))


        part1 = 0
        for lock in locks:
            for key in keys:
                summed = []
                for i in range(len(key)):
                    summed.append(key[i] + lock[i])

                if all([True if val <= 5 else False for val in summed]):
                    part1 += 1


                
        part2 = "Deliver The Chronicle"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
