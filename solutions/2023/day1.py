from Table import Table
from time import time

NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "Trebuchet?!"
        self.input = self.getInput(self.day)

    def match_number(self, string: str):
        for number in NUMBERS:
            if string.startswith(number):
                return NUMBERS[number]
        return None
    
    def find_numbers(self, part2: bool = False) -> list:
        numbers = []

        for line in self.input.splitlines():
            digits = []
            for i, letter in enumerate(line):
                try:
                    num = int(letter)
                    digits.append(num)
                except:
                    if not part2:
                        continue

                    segment = line[i:]
                    num = self.match_number(segment)
                    if num is not None:
                        digits.append(num)

            numbers.append(int(''.join([str(digits[0]), str(digits[-1])])))

        return numbers
                    

    def solve(self):
        start_time = time()

        part1 = sum(self.find_numbers())
        part2 = sum(self.find_numbers(True))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
