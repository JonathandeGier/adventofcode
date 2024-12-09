from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "Print Queue"
        self.input = self.getInput(self.day)

        self.edges = []

    def topological_sort(self, nodes: list, edges: list) -> list:
        result = []
        freeNodes = [node for node in nodes if sum([1 for edge in edges if edge[1] == node]) == 0]

        while len(freeNodes) > 0:
            node = freeNodes.pop()
            result.append(node)

            nextEdges = [edge for edge in edges if edge[0] == node]
            for edge in nextEdges:
                edges.remove(edge)

                otherNode = edge[1]
                otherIncoming = [edge for edge in edges if edge[1] == otherNode]
                if len(otherIncoming) == 0:
                    freeNodes.append(otherNode)
        
        assert len(edges) == 0, 'Cycle detected'

        return result

    def solve(self):
        start_time = time()

        edges, pageSets = self.input.split('\n\n')
        for line in edges.splitlines():
            l, r = line.split('|')
            self.edges.append((int(l), int(r)))

        part1 = 0
        part2 = 0
        for pages in pageSets.splitlines():
            nodes = [int(page) for page in pages.split(',')]
            relevantEdges = [edge for edge in self.edges if edge[0] in nodes and edge[1] in nodes]

            print_order = self.topological_sort(nodes, relevantEdges)

            if nodes == print_order:
                part1 += print_order[len(print_order) // 2]
            else:
                part2 += print_order[len(print_order) // 2]



        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
