from Table import Table
from time import time

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "High-Entropy Passphrases"
        self.input = self.getInput(self.day)

    def get_passphrases(self):
        return [line.split(' ') for line in self.input.splitlines()]

    def solve(self):
        start_time = time()

        passphrases = self.get_passphrases()

        part1 = sum([1 for line in passphrases if len(line) == len(set(line))])

        # sort the passphrase words
        passphrases = [[''.join(sorted(word)) for word in passphrase] for passphrase in passphrases]

        part2 = sum([1 for line in passphrases if len(line) == len(set(line))])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
