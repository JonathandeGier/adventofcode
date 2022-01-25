import math
from typing import Counter
from Table import Table
from time import time

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Infinite Elves and Infinite Houses"
        self.input = self.getInput(self.day)

    def get_presents(self):
        return int(self.input.strip())

    def get_factors(self, number: int):
        factors = []
        for num in range(1, int(math.sqrt(number)) + 1):
            if number % num == 0:
                factors.append(num)
                if number // num != num:
                    factors.append(number // num)
        return factors


    def presents_at_house(self, house: int):
        result = sum(self.get_factors(house)) * 10
        return result


    def new_presents_at_house(self, house: int, visited: dict):
        factors = self.get_factors(house)
        visiting_elfs = []

        for factor in factors:
            if factor not in visited:
                visiting_elfs.append(factor)
                visited[factor] = 1
                continue

            if visited[factor] < 50:
                visiting_elfs.append(factor)
                visited[factor] += 1
                continue

        return sum(visiting_elfs) * 11

    def solve(self):
        start_time = time()

        presents = self.get_presents()
        house = 0

        while True:
            house += 1

            house_presents = self.presents_at_house(house)
            if house_presents >= presents:
                break

        part1 = house

        house = 0
        visited = {}
        while True:
            house += 1

            house_presents = self.new_presents_at_house(house, visited)
            if house_presents >= presents:
                break

        part2 = house

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
