from Table import Table
from time import time
from collections import deque, defaultdict

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Reactor"
        self.input = self.getInput(self.day)

    def invert_devices(self, devices):
        incoming_devices = {}
        for device in devices:
            if device not in incoming_devices:
                incoming_devices[device] = []

            for other_device in devices[device]:
                if other_device not in incoming_devices:
                    incoming_devices[other_device] = []

                incoming_devices[other_device].append(device)
        return incoming_devices

    def solve(self):
        start_time = time()

        # Input parsing
        devices = {}
        for line in self.input.splitlines():
            device, connected = line.split(': ')
            devices[device] = tuple(c for c in connected.split(' '))

        # Part 1: simple BFS
        part1 = 0
        queue = deque(['you'])
        while queue:
            device = queue.popleft()

            if device == 'out':
                part1 += 1
                continue

            for other_device in devices[device]:
                queue.append(other_device)

        # Part 2
        # Invert the devices object, so each key lists the incoming devices
        incoming_devices = self.invert_devices(devices)

        # Make a topological sorting of the devices using Kahn's algorithm
        sorted_devices = []
        devices_without_incoming = [device for device in incoming_devices if len(incoming_devices[device]) == 0]

        while devices_without_incoming:
            device = devices_without_incoming.pop()
            sorted_devices.append(device)

            for other_device in incoming_devices:
                if device in incoming_devices[other_device]:
                    incoming_devices[other_device].remove(device)
                    if len(incoming_devices[other_device]) == 0:
                        devices_without_incoming.append(other_device)

        # This code only works for non-cyclical graphs
        if not all([len(incoming_devices[device]) == 0 for device in incoming_devices]):
            assert False, "Graph has a cycle"

        # re-invert the devices, since it was edited in the topological sorting and is needed later
        incoming_devices = self.invert_devices(devices)

        # For each node, remember how many paths can be taken to get to that node
        # default: nr. paths through any node
        # dac: nr. paths through the dac node
        # fft: nr. paths through the fft node
        # dac_fft: nr. paths through both the dac and fft node
        paths = {}
        paths['svr'] = {'default': 1, 'dac': 0, 'fft': 0, 'dac_fft': 0}

        # Step through all (sorted) devices
        for device in sorted_devices:
            if device not in paths:
                paths[device] = {'default': 0, 'dac': 0, 'fft': 0, 'dac_fft': 0}

            for other_device in incoming_devices[device]:
                if device == 'dac':
                    # When going through the dac node, all default paths now get added to the dac node and all fft paths now get added to the dac_fft paths
                    paths[device]['default'] += paths[other_device]['default']
                    paths[device]['dac'] += paths[other_device]['default']
                    paths[device]['fft'] += paths[other_device]['fft']
                    paths[device]['dac_fft'] += paths[other_device]['fft']
                elif device == 'fft':
                    # When going through the fft node, all default paths now get added to the fft node and all dac paths now get added to the dac_fft paths
                    paths[device]['default'] += paths[other_device]['default']
                    paths[device]['dac'] += paths[other_device]['dac']
                    paths[device]['fft'] += paths[other_device]['default']
                    paths[device]['dac_fft'] += paths[other_device]['dac']
                else:
                    # default case: each key adds to itself
                    paths[device]['default'] += paths[other_device]['default']
                    paths[device]['dac'] += paths[other_device]['dac']
                    paths[device]['fft'] += paths[other_device]['fft']
                    paths[device]['dac_fft'] += paths[other_device]['dac_fft']

        part2 = paths['out']['dac_fft']

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
