from Table import Table
from time import time

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Lens Library"
        self.input = self.getInput(self.day).strip()


    def hash(self, string: str) -> int:
        val = 0
        for char in string:
            val += ord(char)
            val *= 17
            val %= 256
        return val
    

    def indexOfLabel(self, lenses: list, label: str) -> int:
        for i, lens in enumerate(lenses):
            if lens[0] == label:
                return i
        return -1


    def initialization_sequence(self) -> list:
        boxes = [[] for _ in range(256)]
        for step in self.input.split(','):
            if '=' in step:
                operation = '='
                parts = step.split('=')
                label = parts[0]
                focal_length = int(parts[1])
            else:
                assert '-' in step
                operation = '-'
                label = step.split('-')[0]
            
            box = self.hash(label)
            if operation == '=':
                i = self.indexOfLabel(boxes[box], label)
                if i == -1:
                    boxes[box].append([label, focal_length])
                else:
                    boxes[box][i][1] = focal_length
            else:
                i = self.indexOfLabel(boxes[box], label)
                if i != -1:
                    del boxes[box][i]
        return boxes


    def focus_power(self, boxes: list) -> int:
        focus_power = 0
        for box_i, box in enumerate(boxes):
            for lens_i, lens in enumerate(box):
                focus_power += ((box_i + 1) * (lens_i + 1) * lens[1])
        return focus_power


    def solve(self):
        start_time = time()

        part1 = sum([self.hash(string) for string in self.input.split(',')])

        boxes = self.initialization_sequence()
        part2 = self.focus_power(boxes)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
