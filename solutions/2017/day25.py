from collections import defaultdict
from Table import Table
from time import time

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "The Halting Problem"
        self.input = self.getInput(self.day)

        self.start_state = None
        self.steps = 0
        self.behavior = {}

    def get_machine(self):
        parafs = self.input.split("\n\n")
        self.start_state = parafs[0].splitlines()[0].split(' ')[-1][0:1]
        self.steps = int(parafs[0].splitlines()[1].split(' ')[-2])
        
        # todo: generalize solution
        self.behavior = {
            'A': {0: (1, 1, 'B'), 1: (0, -1, 'B')},
            'B': {0: (0, 1, 'C'), 1: (1, -1, 'B')},
            'C': {0: (1, 1, 'D'), 1: (0, -1, 'A')},
            'D': {0: (1, -1, 'E'), 1: (1, -1, 'F')},
            'E': {0: (1, -1, 'A'), 1: (0, -1, 'D')},
            'F': {0: (1, 1, 'A'), 1: (1, -1, 'E')},
        }

    def run(self):
        strip = defaultdict(lambda: 0)
        cursor = 0
        state = self.start_state

        for _ in range(self.steps):
            if state not in self.behavior:
                assert False, 'Invalid state: ' + str(state)

            case = self.behavior[state]
            value = strip[cursor]
            if value not in case:
                assert False, 'Invalid strip value: ' + str(value)

            strip[cursor] = case[value][0]
            cursor += case[value][1]
            state = case[value][2]

        return sum(strip.values())


    def solve(self):
        start_time = time()

        self.get_machine()

        part1 = self.run()
        part2 = "Reboot the printer!"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
