from Table import Table
from time import time

class Layer:

    def __init__(self, layer: int, depth: int):
        self.layer = layer
        self.depth = depth
        self.cycle = depth + depth - 2


class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Packet Scanners"
        self.input = self.getInput(self.day)

    def load_firewall(self):
        firewall = []
        for line in self.input.splitlines():
            segments = line.split(': ')
            layer = int(segments[0])
            depth = int(segments[1])

            firewall.append(Layer(layer, depth))

        return firewall

    def solve(self):
        start_time = time()

        firewall = self.load_firewall()

        part1 = sum([layer.layer * layer.depth for layer in firewall if layer.layer % layer.cycle == 0])

        part2 = "None"

        delay = 0
        result = 1
        while result > 0:
            delay += 1
            if delay % 20000 == 0:
                self.printRow((self.day, self.title, part1, delay, ''), end="\r")
            result = sum([1 for layer in firewall if (layer.layer + delay) % layer.cycle == 0])

        part2 = delay

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
