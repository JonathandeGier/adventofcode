from Table import Table
from time import time

# _md5 implementation runs about 10 seconds faster than hashlib (~30% improvement)
import hashlib
from _md5 import md5

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "How About a Nice Game of Chess?"
        self.input = self.getInput(self.day).strip()

    def starts_with_5_zeros(self, string):
        return len(string) >= 5 and string[0] == "0" and string[1] == "0" and string[2] == "0" and string[3] == "0" and string[4] == "0"

    def solve(self):
        start_time = time()

        password1 = []
        password2 = ["_", "_", "_", "_", "_", "_", "_", "_"]
        i = 0
        while "_" in password2:
            word = self.input + str(i)
            # hash = hashlib.md5(word.encode()).hexdigest()
            hash = md5(word.encode()).hexdigest()
            if self.starts_with_5_zeros(hash):
                if len(password1) < 8:
                    password1.append(hash[5])
                
                if hash[5] in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                    index = int(hash[5])
                    if password2[index] == "_":
                        password2[index] = hash[6]

            i += 1


        part1 = "".join(password1)
        part2 = "".join(password2)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
