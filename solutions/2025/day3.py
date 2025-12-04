from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Lobby"
        self.input = self.getInput(self.day)

    def max_jolts(self, bank: list, digits: int) -> int:
        batteries = []
        left = 0
        right = len(bank) - digits + 1
        for i in range(digits):
            max_battery = max(bank[left:right])
            index = bank.index(max_battery, left, right)
            batteries.append(max_battery)
            
            left = index + 1
            right += 1

        return int(''.join([str(x) for x in batteries]))

    def solve(self):
        start_time = time()

        part1 = 0
        part2 = 0
        for bank in self.input.splitlines():
            bank = [int(x) for x in bank]

            part1 += self.max_jolts(bank, 2)
            part2 += self.max_jolts(bank, 12)


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
