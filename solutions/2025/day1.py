from Table import Table
from time import time

class Day0(Table):

    def __init__(self):
        self.day = 1
        self.title = "Secret Entrance"
        self.input = self.getInput(self.day).splitlines()

    def solve(self):
        start_time = time()

        part1 = 0
        part2 = 0
        current = 50
        for move in self.input:
            direction, number = move[0], int(move[1:])

            if direction == "L":
                [div, remainder] = divmod(current - number, 100)
                part2 += abs(div)

                if current == 0 and remainder > 0:
                    part2 -= 1
                elif current > 0 and remainder == 0:
                    part2 += 1

                current = remainder
            else:
                [div, remainder] = divmod(current + number, 100)
                part2 += div
                current = remainder
            
            if current == 0:
                part1 += 1


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day0()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
