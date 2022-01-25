from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "Doesn't He Have Intern-Elves For This?"
        self.input = self.getInput(self.day)

    def get_strings(self):
        return self.input.splitlines()

    # Puzzle 1 conditions
    def contains_vowels(self, string):
        a = string.count("a")
        e = string.count("e")
        i = string.count("i")
        o = string.count("o")
        u = string.count("u")
        return a + e + i + o + u >= 3

    def contains_double(self, string):
        for i in range(len(string) - 1):
            if string[i] == string[i + 1]:
                return True
        return False

    def does_not_contain(self, string):
        contains = "ab" in string or "cd" in string or "pq" in string or "xy" in string
        return not contains

    # Puzzle 2 conditions
    def contains_pair(self, string):
        for i in range(len(string) - 1):
            substr = string[i:i+2]
            if len(string.split(substr)) >= 3:
                return True
        return False

    def contains_repeating_char(self, string):
        for i in range(len(string) - 2):
            if string[i] == string[i + 2]:
                return True
        return False

    def solve(self):
        start_time = time()

        part1 = 0
        for string in self.get_strings():
            if self.contains_vowels(string) and self.contains_double(string) and self.does_not_contain(string):
                part1 += 1

        part2 = 0
        for string in self.get_strings():
            if self.contains_pair(string) and self.contains_repeating_char(string):
                part2 += 1
        
        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
