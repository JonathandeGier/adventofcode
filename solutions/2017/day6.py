from Table import Table
from time import time

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Memory Reallocation"
        self.input = self.getInput(self.day)

    def get_banks(self):
        return [int(val) for val in self.input.split("\t")]

    def solve(self):
        start_time = time()

        banks = self.get_banks()
        seen_states = {}
        cycles = 0
        seen_states[tuple(banks)] = 0
        
        while True:
            max_val = max(banks)

            for i in range(len(banks)):
                if banks[i] == max_val:
                    break

            val = banks[i]
            banks[i] = 0

            while val > 0:
                i += 1
                banks[i % len(banks)] += 1
                val -= 1

            cycles += 1

            state = tuple(banks)
            if state in seen_states:
                break
            seen_states[state] = cycles



        part1 = cycles
        part2 = cycles - seen_states[state]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
