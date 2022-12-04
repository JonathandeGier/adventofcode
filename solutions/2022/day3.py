from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Rucksack Reorganization"
        self.input = self.getInput(self.day)

    def get_backpacks(self):
        backpacks = []
        for line in self.input.splitlines():
            assert len(line) % 2 == 0
            backpacks.append((line[:len(line) // 2], line[len(line) // 2:]))

        return backpacks

    def group_backpacks(self):
        groups = []
        lines = self.input.splitlines()
        for i in range(0, len(lines), 3):
            groups.append(tuple(lines[i:i+3]))

        return groups

    def priority(self, letter: str):
        is_upper = letter == letter.upper()

        priority = ord(letter.lower()) - 96
        if is_upper:
            priority += 26

        return priority

    def solve(self):
        start_time = time()

        backpacks = self.get_backpacks()

        part1 = 0
        for backpack in backpacks:
            common_letter = None
            for letter in backpack[0]:
                if letter in backpack[1]:
                    common_letter = letter
                    break
            
            assert common_letter != None

            part1 += self.priority(common_letter)

        backpack_groups = self.group_backpacks()
        
        part2 = 0
        for backpack_group in backpack_groups:
            common_letter = None
            for letter in backpack_group[0]:
                if letter in backpack_group[1] and letter in backpack_group[2]:
                    common_letter = letter

            assert letter != None

            part2 += self.priority(common_letter)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
