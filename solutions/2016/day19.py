from collections import deque
from math import floor
from textwrap import dedent
from turtle import left
from Table import Table
from time import time

class Elf:
    def __init__(self, startpos: int, presents: int):
        self.startpos = startpos
        self.presents = presents
        self.left = None

    def setLeft(self, newLeft):
        self.left = newLeft

    def __eq__(self, other):
        return type(other) == Elf and other.startpos == self.startpos

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "An Elephant Named Joseph"
        self.input = int(self.getInput(self.day).strip())


    def solve(self):
        start_time = time()

        # Build the circle
        startElf = Elf(1, 1)
        prev = startElf
        for i in range(2, self.input + 1):
            prev.setLeft(Elf(i, 1))
            prev = prev.left
        
        prev.setLeft(startElf)

        # Part 1: take presents from the elf to the left
        currentElf = startElf
        while currentElf.left != currentElf:
            currentElf.presents += currentElf.left.presents
            currentElf.left = currentElf.left.left
            currentElf = currentElf.left

        part1 = currentElf.startpos

        # Rebuild the circle
        startElf = Elf(1, 1)
        prev = startElf
        for i in range(2, self.input + 1):
            prev.setLeft(Elf(i, 1))
            prev = prev.left
        
        prev.setLeft(startElf)

        # Part 2: take presents from the elf across
        size = self.input
        currentElf = startElf
        elfBeforeAcross = currentElf
        ahead = 0

        while currentElf.left != currentElf:
            desiredAhead = floor(size / 2) - 1
            diff = desiredAhead - ahead
            assert diff >= 0

            for _ in range(diff):
                elfBeforeAcross = elfBeforeAcross.left
                ahead += 1


            currentElf.presents += elfBeforeAcross.left.presents
            elfBeforeAcross.left = elfBeforeAcross.left.left
            size -= 1

            currentElf = currentElf.left
            ahead -= 1

        part2 = currentElf.startpos

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
