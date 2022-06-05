from Table import Table
from time import time

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Inverse Captcha"
        self.input = self.getInput(self.day)

    def get_capcha(self):
        return [int(val) for val in self.input.splitlines()[0]]

    def solve(self):
        start_time = time()

        capcha = self.get_capcha()

        sum = 0
        for i in range(len(capcha)):
            val1 = capcha[i]
            val2 = capcha[(i + 1) % len(capcha)]

            if val1 == val2:
                sum += val1

        part1 = sum

        sum2 = 0
        for i in range(len(capcha)):
            val1 = capcha[i]
            val2 = capcha[(i + (len(capcha) // 2)) % len(capcha)]

            if val1 == val2:
                sum2 += val1

        part2 = sum2

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
