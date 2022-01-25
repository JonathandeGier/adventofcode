from Table import Table
from time import time

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Corporate Policy"
        self.input = self.getInput(self.day)

    def get_password(self):
        return self.input.strip()

    def increment(self, string: str, index = -1):
        try:
            char = string[index]
        except IndexError:
            return "a" + string

        next_char = self.next_alpha(char)
        
        s = list(string)
        s[index] = next_char
        string = "".join(s)
        
        if next_char == "a":
            string = self.increment(string, index - 1)

        return string

    def next_alpha(self, s):
        return chr((ord(s.upper())+1 - 65) % 26 + 65).lower()


    def has_incrementing_straight(self, string: str):
        for i in range(len(string) - 2):
            char0 = ord(string[i])
            char1 = ord(string[i + 1])
            char2 = ord(string[i + 2])

            if char1 - char0 == 1 and char2 - char1 == 1:
                return True
        return False

    def does_not_contain_illegal_letters(self, string: str):
        if "i" in string or "o" in string or "l" in string:
            return False
        return True

    def contains_non_overlapping_pair(self, string: str):
        for i in range(len(string) - 1):
            char0 = string[i]
            char1 = string[i + 1]
            
            if char0 == char1 and i + 3 <= len(string) - 1:
                substr = string[i + 2:]
                for j in range(len(substr) - 1):
                    char2 = substr[j]
                    char3 = substr[j + 1]

                    if char2 == char3:
                        return True
        return False

    def valid_password(self, string):
        return self.has_incrementing_straight(string) and self.does_not_contain_illegal_letters(string) and self.contains_non_overlapping_pair(string)

    def solve(self):
        start_time = time()

        password = self.get_password()

        while not self.valid_password(password):
            password = self.increment(password)

        part1 = password

        password = self.increment(password)
        while not self.valid_password(password):
            password = self.increment(password)
        
        part2 = password

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
