from Table import Table
from time import time
import hashlib

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "The Ideal Stocking Stuffer"
        self.input = Table.getInput(self.day)

    def get_lines(self):
        lines = self.input.splitlines()
        return lines

    def starts_with_5_zeros(self, string):
        return len(string) >= 5 and string[0] == "0" and string[1] == "0" and string[2] == "0" and string[3] == "0" and string[4] == "0"

    def starts_with_6_zeros(self, string):
        return len(string) >= 6 and string[0] == "0" and string[1] == "0" and string[2] == "0" and string[3] == "0" and string[4] == "0" and string[5] == "0"

    def solve(self):
        start_time = time()

        key = self.input.strip()
        i = 0
        string = key + str(i)
        hash = hashlib.md5(string.encode()).hexdigest()

        while not self.starts_with_5_zeros(hash):
            i += 1
            string = key + str(i)
            hash = hashlib.md5(string.encode()).hexdigest()

        part1 = i

        while not self.starts_with_6_zeros(hash):
            i += 1
            string = key + str(i)
            hash = hashlib.md5(string.encode()).hexdigest()

        part2 = i

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
