from Table import Table
from time import time
from hashlib import md5

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "One-Time Pad"
        self.input = self.getInput(self.day).strip()

    def three_of_a_kind(self, hash):
        results = []
        for i in range(len(hash) - 2):
            if hash[i] == hash[i+1] and hash[i+1] == hash[i+2]:
                results.append(hash[i:i+3])
                return results

        return results

    def five_of_a_kind(self, hash):
        results = []
        for i in range(len(hash) - 4):
            if hash[i] == hash[i+1] and hash[i+1] == hash[i+2] and hash[i+2] == hash[i+3] and hash[i+3] == hash[i+4]:
                results.append(hash[i:i+5])
                return results

        return results

    def is_upper(self, string: str):
        for char in string:
            if char.isupper():
                return True
        return False

    def find_keys(self, count: int, rounds: int):
        potential_keys = [] # [{ three-of-a-kind => index }]
        confirmed_keys = [] # [{ three-of-a-kind => index, five-of-a-kind => index }]

        i = 0
        while len(confirmed_keys) < count:
            hash = self.input + str(i)

            for _ in range(rounds):
                hash = md5(hash.encode()).hexdigest()

            if self.is_upper(hash):
                print(hash)

            toaks = self.three_of_a_kind(hash)
            foaks = self.five_of_a_kind(hash)

            for foak in foaks:
                three_key = foak[0] + foak[0] + foak[0]
                correct_keys = [key for key in potential_keys if three_key in key and i - key[three_key] <= 1000]
                
                for confirmed_key in correct_keys:
                    confirmed_key[foak] = i
                    confirmed_keys.append((confirmed_key[three_key], confirmed_key))
                
                potential_keys = [key for key in potential_keys if foak not in key]

            # add three of a kinds to potential keys
            for pok in toaks:
                potential_keys.append({pok: i})

            i += 1

        confirmed_keys.sort()
        return confirmed_keys[:count]


    def solve(self):
        start_time = time()

        part1 = self.find_keys(64, 1)[-1][0]

        part2 = self.find_keys(64, 2017)[-1][0]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
