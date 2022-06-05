from typing import Counter
from Table import Table
from time import time

class Program:

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        
        self.parent = None
        self.children = []

    def total_weight(self):
        return self.weight + sum([child.total_weight() for child in self.children])

    def balanced_weight(self):
        if len(self.children) == 0:
            return False

        counter = Counter([child.total_weight() for child in self.children])
        return counter.most_common()[0][0]

    def unbalanced_child(self):
        if self.is_balanced():
            return None

        assert len(self.children) > 2

        counter = Counter([child.total_weight() for child in self.children])
        unbalanced_weight = counter.most_common()[-1][0]

        unbalanced_program = [child for child in self.children if child.total_weight() == unbalanced_weight][0]
        return unbalanced_program
        

    def is_balanced(self):
        if len(self.children) == 0:
            return True
        else:
            return len(set([child.total_weight() for child in self.children])) == 1

    def __str__(self):
        return f"{self.name} - ({self.weight}) - [{len(self.children)}, ({[[child.total_weight() for child in self.children]]})]"


class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Recursive Circus"
        self.input = self.getInput(self.day)

    def get_tree(self):
        # get each program and their weights
        programs = {}
        for line in self.input.splitlines():
            segments = line.split(' ')
            program = Program(segments[0], int(segments[1][1:-1]))
            programs[program.name] = program

        # assign the children
        for line in self.input.splitlines():
            if '->' not in line:
                continue

            program = programs[line.split(' ')[0]]
            children = line.split(' -> ')[1].split(', ')

            for child in children:
                child_program = programs[child]
                child_program.parent = program
                program.children.append(child_program)

        return programs


    def solve(self):
        start_time = time()

        programs = self.get_tree()

        bottom_program = [programs[prog] for prog in programs if programs[prog].parent is None][0]

        part1 = bottom_program.name

        unbalanced_program = bottom_program
        while unbalanced_program.unbalanced_child() is not None:
            unbalanced_program = unbalanced_program.unbalanced_child()

        total_weight_to_be = unbalanced_program.parent.balanced_weight()
        weight_to_be = total_weight_to_be - sum([child.total_weight() for child in unbalanced_program.children])
        part2 = weight_to_be

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
