from Table import Table
from time import time
from itertools import product

PRICE_CACHE = {}

class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Monkey Market"
        self.input = self.getInput(self.day)


    def next_secret(self, number: int) -> int:
        number = (number ^ (number * 64)) % 16777216
        number = (number ^ (number // 32)) % 16777216
        number = (number ^ (number * 2048)) % 16777216
        return number
    

    def solve(self):
        start_time = time()

        initial_values = [int(val) for val in self.input.splitlines()]

        part1 = 0
        all_changes = set()
        for initial_secret in initial_values:
            PRICE_CACHE[initial_secret] = {}
            
            secret = initial_secret
            old_price = secret % 10
            changes = (None, None, None, None)
            for _ in range(2000):
                secret = self.next_secret(secret)
                new_price = secret % 10

                changes = (changes[1], changes[2], changes[3], new_price - old_price)
                all_changes.add(changes)
                if changes not in PRICE_CACHE[initial_secret]:
                    PRICE_CACHE[initial_secret][changes] = new_price

                old_price = new_price

            part1 += secret


        part2 = 0
        for sequence in all_changes:
            bananas = 0
            for initial_secret in initial_values:
                if sequence in PRICE_CACHE[initial_secret]:
                    bananas += PRICE_CACHE[initial_secret][sequence]

            part2 = max(part2, bananas)


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
