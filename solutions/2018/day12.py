from collections import defaultdict
from Table import Table
from time import time

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Subterranean Sustainability"
        self.input = self.getInput(self.day)
        self.rules = {}

    def get_data(self):
        lines = self.input.splitlines()

        plants = lines[0].split(': ')[1]

        rules = {}
        for rule in lines[2:]:
            rule_segments = rule.split(' => ')
            rules[rule_segments[0]] = rule_segments[1]

        return plants, rules

    def simulate(self, state: str, first_pot: int, iterations: int):
        def get_val(string: str, index: int):
            if index >= 0 and index < len(string):
                return string[index]
            return '.'

        for current in range(iterations):
            last = state
            last_first_pot = first_pot

            first_pot = first_pot - 2
            new_state = ''
            for i in range(-2, len(state) + 2):
                segment = ''.join([get_val(state, i-2), get_val(state, i-1), get_val(state, i), get_val(state, i+1), get_val(state, i+2)])
                new_state = new_state + self.rules[segment]

            first_pot = first_pot + new_state.find('#')
            state = new_state.strip('.')

            if state == last:
                pot_diff = first_pot - last_first_pot
                iterations_left = iterations - (current + 1)
                first_pot = first_pot + (pot_diff * iterations_left)
                break

        return state, first_pot

    def solve(self):
        start_time = time()

        initial_state, rules = self.get_data()
        self.rules = rules

        final_gen, start_pot = self.simulate(initial_state, 0, 20)
        part1 = sum([start_pot + item[0] for item in enumerate(final_gen) if item[1] == '#'])

        final_gen, start_pot = self.simulate(initial_state, 0, 50_000_000_000)
        part2 = sum([start_pot + item[0] for item in enumerate(final_gen) if item[1] == '#'])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
