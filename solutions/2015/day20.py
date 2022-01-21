from typing import Counter
from getInput import get_input

import math


def get_presents():
    return int(get_input(2015, 20).strip())


def get_factors(number: int):
    factors = []
    for num in range(1, int(math.sqrt(number)) + 1):
        if number % num == 0:
            factors.append(num)
            if number // num != num:
                factors.append(number // num)
    return factors


def presents_at_house(house: int):
    result = sum(get_factors(house)) * 10
    return result


def new_presents_at_house(house: int, visited: dict):
    factors = get_factors(house)
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


def main():
    presents = get_presents()
    house = 0

    while True:
        house += 1

        house_presents = presents_at_house(house)
        if house_presents >= presents:
            break
    
    print("Puzzle 1:")
    print(house)

    print("")

    house = 0
    visited = {}
    while True:
        house += 1

        house_presents = new_presents_at_house(house, visited)
        if house_presents >= presents:
            break

    print("Puzzle 2:")
    print(house)


if __name__ == "__main__":
    main()
