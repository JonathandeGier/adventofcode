from Table import Table
from time import time

class Program:

    def __init__(self, id: int):
        self.id = id
        self.connected = []

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Digital Plumber"
        self.input = self.getInput(self.day)

    def load_programs(self):
        programs = {}
        for line in self.input.splitlines():
            id = int(line.split(' <-> ')[0])
            programs[id] = Program(id)

        for line in self.input.splitlines():
            segments = line.split(' <-> ')
            id = int(segments[0])
            programs[id].connected = [programs[int(val)] for val in segments[1].split(',')]

        return programs


    def solve(self):
        start_time = time()

        programs = self.load_programs()

        all_ids = set(range(2000))
        found = set()
        groups = []

        while len(all_ids) > len(found):
            program = programs[list(all_ids.difference(found))[0]]

            group = set()
            queue = []

            queue.append(program)
            while len(queue) > 0:
                program = queue.pop()

                if program.id in group:
                    continue

                group.add(program.id)
                found.add(program.id)

                for connected_program in program.connected:
                    if connected_program.id in group:
                        continue

                    queue.append(connected_program)

            groups.append(group)

        part1 = len(groups[0])
        part2 = len(groups)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
