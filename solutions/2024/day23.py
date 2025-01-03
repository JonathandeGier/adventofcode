from Table import Table
from time import time
from itertools import permutations, combinations

class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "LAN Party"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        edges = set()
        connected_computers = {}
        for line in self.input.splitlines():
            nodeA, nodeB = line.split('-')

            edges.add((nodeA, nodeB))
            edges.add((nodeB, nodeA))

            if nodeA not in connected_computers:
                connected_computers[nodeA] = []
            if nodeB not in connected_computers:
                connected_computers[nodeB] = []

            connected_computers[nodeA].append(nodeB)
            connected_computers[nodeB].append(nodeA)


        connected_tripples = set()
        for node, connected in connected_computers.items():
            if len(connected) < 2:
                continue
            if node[0] != 't':
                continue

            for node2 in connected:
                for node3 in connected:
                    if node2 == node3:
                        continue

                    if (node2, node3) in edges:
                        key = tuple(sorted([node, node2, node3]))
                        connected_tripples.add(key)
        
        part1 = len(connected_tripples)

        largest_network = set()
        for node1, connected in connected_computers.items():
            if len(connected) < 2:
                continue

            for node2 in connected:
                network = set()
                network.add(node1)
                network.add(node2)
                for new_node in connected:
                    if new_node == node2:
                        continue

                    all_connected = True
                    for network_node in network:
                        if (new_node, network_node) not in edges:
                            all_connected = False
                            break

                    if all_connected:
                        network.add(new_node)

                if len(largest_network) < len(network):
                    largest_network = network


        part2 = ','.join(sorted(largest_network))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
