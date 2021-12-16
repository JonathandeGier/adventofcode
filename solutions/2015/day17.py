from typing import Counter
from getInput import get_input
from itertools import combinations
import math

def get_sizes():
    input = get_input(2015, 17).splitlines()
    return [int(x) for x in input]


def main():
    containers = get_sizes()
    target = 150

    result = [seq for i in range(len(containers), 0, -1)
          for seq in combinations(containers, i)
          if sum(seq) == target]

    print("Puzzle 1:")
    print(len(result))

    print("")

    print("Puzzle 2:")
    count = Counter([len(x) for x in result])
    lowest_key = min(count.keys())
    print(count[lowest_key])


if __name__ == "__main__":
    main()
