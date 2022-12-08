from Table import Table
from time import time

class Directory:
    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.content = []

    def add_item(self, item):
        self.content.append(item)

    def get_dir(self, dir_name):
        return [item for item in self.content if type(item) == Directory and item.name == dir_name][0]

    def get_directories(self):
        return [item for item in self.content if type(item) == Directory]

    def tree(self):
        dirs = [self]
        for dir in self.get_directories():
            dirs += dir.tree()

        return dirs

    def get_size(self):
        return sum([item.get_size() for item in self.content])

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size


class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "No Space Left On Device"
        self.input = self.getInput(self.day)

        self.root = Directory('', None)

    def load_file_system(self):
        self.root = Directory('', None)

        current_dir = None

        for line in self.input.splitlines():
            segments = line.split(' ')

            if segments[0] == '$':
                if segments[1] == 'cd':
                    if segments[2] == '/':
                        current_dir = self.root
                    elif segments[2] == '..':
                        current_dir = current_dir.parent
                    else:
                        current_dir = current_dir.get_dir(segments[2])
                
                continue

            if segments[0] == 'dir':
                current_dir.add_item(Directory(segments[1], current_dir))
            else:
                current_dir.add_item(File(segments[1], int(segments[0])))

    def solve(self):
        start_time = time()

        self.load_file_system()

        part1 = sum([dir.get_size() for dir in self.root.tree() if dir.get_size() <= 100_000])

        total_space = 70_000_000
        needed_space = 30_000_000
        current_space = total_space - self.root.get_size()
        required_space_deleted = needed_space - current_space

        part2 = min([dir.get_size() for dir in self.root.tree() if dir.get_size() >= required_space_deleted])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
