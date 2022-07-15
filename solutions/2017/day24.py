from Table import Table
from time import time

class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Electromagnetic Moat"
        self.input = self.getInput(self.day)

        self.max_strength = 0
        self.longest = 0
        self.longest_max_strength = 0

    def get_components(self):
        components = set()
        for line in self.input.splitlines():
            a, b = line.split('/')
            components.add((int(a), int(b)))

        return components

    def link(self, components: set, bridge: list):
        if len(bridge) == 0:
            num_to_link = 0
        elif len(bridge) == 1:
            num_to_link = max(bridge[-1])
        else:
            if bridge[-1][0] in bridge[-2]:
                num_to_link = bridge[-1][1]
            elif bridge[-1][1] in bridge[-2]:
                num_to_link = bridge[-1][0]
            else:
                assert False, 'invalid bridge'

        possible_components = [comp for comp in components if comp[0] == num_to_link or comp[1] == num_to_link]
        
        if len(possible_components) == 0:
            length = len(bridge)
            strength = sum([sum(component) for component in bridge])

            self.max_strength = max(self.max_strength, strength)

            if length > self.longest:
                self.longest = length
                self.longest_max_strength = strength
            elif length == self.longest:
                self.longest_max_strength = max(self.longest_max_strength, strength)


        for component in possible_components:
            bridge.append(component)
            components.remove(component)
            self.link(components, bridge)
            bridge.pop()
            components.add(component)

    def solve(self):
        start_time = time()
        components = self.get_components()

        self.link(components, [])

        part1 = self.max_strength
        part2 = self.longest_max_strength

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
