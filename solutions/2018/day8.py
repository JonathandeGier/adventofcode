from Table import Table
from time import time

class Node():

    def __init__(self, header: tuple):
        self.parent = None
        self.header = header
        self.children = []
        self.metadata = None

    def meta_sum(self) -> int:
        return sum([child.meta_sum() for child in self.children]) + sum(self.metadata)

    def value(self) -> int:
        if len(self.children) == 0:
            return sum(self.metadata)
        
        val = 0
        for i in self.metadata:
            i -= 1
            if i >= 0 and i < len(self.children):
                val += self.children[i].value()

        return val

    def __str__(self) -> str:
        return str(self.header) + ' - ' + str(len(self.children)) + ' - ' + str(self.metadata)

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Memory Maneuver"
        self.input = self.getInput(self.day)
        self.numbers = None

    def get_node(self, index) -> tuple:
        header = tuple(self.numbers[index:index+2])

        node = Node(header)

        index += 2
        for _ in range(header[0]):
            child_node, new_index = self.get_node(index)
            
            child_node.parent = node
            node.children.append(child_node)
            
            index = new_index

        node.metadata = tuple(self.numbers[index:index + header[1]])
        index += header[1]

        return node, index


    def solve(self):
        start_time = time()

        self.numbers = [int(num) for num in self.input.split(' ')]

        root, _ = self.get_node(0)
        

        part1 = root.meta_sum()
        part2 = root.value()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
