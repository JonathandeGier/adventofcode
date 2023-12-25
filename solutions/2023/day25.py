from Table import Table
from time import time
import networkx as nx

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Snowverload"
        self.input = self.getInput(self.day)

        self.graph = None

    def parse_graph(self):
        self.graph = nx.Graph()

        for line in self.input.splitlines():
            component, connections = line.split(': ')
            for connection in connections.split(' '):
                self.graph.add_edge(component, connection)


    def split_graph(self):
        centrality = nx.algorithms.centrality.edge_betweenness_centrality(self.graph)
        
        edges_to_remove = sorted(centrality.items(), key = lambda item:item[1], reverse = True)[:3]
        
        for edge_to_remove in edges_to_remove:
            self.graph.remove_edge(*edge_to_remove[0])

        assert nx.algorithms.components.number_connected_components(self.graph) == 2, 'Removing 3 edges did not split the graph'

        return [len(community) for community in nx.connected_components(self.graph)]

    def solve(self):
        start_time = time()

        self.parse_graph()

        communities = self.split_graph()

        part1 = communities[0] * communities[1]
        part2 = "Push The Big Red Button"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
