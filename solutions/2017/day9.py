from Table import Table
from time import time

class Group:

    def __init__(self):
        self.parent = None
        self.subgroups = []
        self.garbage = []

    def score(self):
        if self.parent is None:
            return 1
        else:
            return self.parent.score() + 1

    def garbage_length(self):
        own_garbage_length = 0
        for garbage_string in self.garbage:
            # remove start and end tags from length calculation
            garbage_string = garbage_string[1:-1]

            # remode ignore characters from length capcluation
            parsed_garbage = []
            ignore_next = False
            for char in garbage_string:
                if ignore_next:
                    ignore_next = False
                    continue

                if char == '!':
                    ignore_next = True
                    continue

                parsed_garbage.append(char)

            own_garbage_length += len(parsed_garbage)

        return own_garbage_length + sum([subgroup.garbage_length() for subgroup in self.subgroups])
        

    def total_score(self):
        return self.score() + sum([subgroup.total_score() for subgroup in self.subgroups])

    def __str__(self):
        return '{' + ','.join([str(subgroup) for subgroup in self.subgroups]) + '}'

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Stream Processing"
        self.input = self.getInput(self.day)[:-1]

    def parse_stream(self):
        
        current_group = Group()
        is_garbage = False
        garbage_string = []
        ignore_next = False
        for char in self.input:
            # Filter out garbage
            if is_garbage:
                garbage_string.append(char)

            if ignore_next:
                ignore_next = False
                continue

            if char == '!':
                ignore_next = True

            if char == '<':
                if not is_garbage:
                    is_garbage = True
                    garbage_string.append(char)
                
            if char == '>':
                is_garbage = False
                current_group.garbage.append(''.join(garbage_string))
                garbage_string = []
                continue

            if is_garbage:
                continue

            # Parse groups
            if char == '{':
                parent_group = current_group
                current_group = Group()
                current_group.parent = parent_group
                parent_group.subgroups.append(current_group)

            if char == '}':
                current_group = current_group.parent


        root = current_group.subgroups[0]
        root.parent = None
        return root


    def solve(self):
        start_time = time()

        root = self.parse_stream()

        part1 = root.total_score()
        part2 = root.garbage_length()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
