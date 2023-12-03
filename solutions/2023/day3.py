from Table import Table
from time import time
from collections import deque

EMPTY = '.'
GEAR = '*'

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Gear Ratios"
        self.input = self.getInput(self.day)

        self.schematic = None

    def parse_schematic(self):
        self.schematic = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val is not EMPTY:
                    self.schematic[x, y] = val

    
    def adjacent(self, pos: tuple):
        return [
            (pos[0] + 1, pos[1] - 1),
            (pos[0] + 1, pos[1]    ),
            (pos[0] + 1, pos[1] + 1),
            (pos[0]    , pos[1] - 1),
            (pos[0]    , pos[1] + 1),
            (pos[0] - 1, pos[1] - 1),
            (pos[0] - 1, pos[1]    ),
            (pos[0] - 1, pos[1] + 1),
        ]
    

    def get_number(self, pos: tuple):
        if pos not in self.schematic or not self.schematic[pos].isdigit():
            assert False, 'Position not a part number'
        
        values = deque()
        visited = set()

        # add the current value
        values.append(self.schematic[pos])
        visited.add(pos)
       
        # get the values to the left
        pointer = (pos[0] - 1, pos[1])
        while pointer in self.schematic and self.schematic[pointer].isdigit():
            values.appendleft(self.schematic[pointer])
            visited.add(pointer)

            pointer = (pointer[0] - 1, pointer[1])

        # get the values to the left
        pointer = (pos[0] + 1, pos[1])
        while pointer in self.schematic and self.schematic[pointer].isdigit():
            values.append(self.schematic[pointer])
            visited.add(pointer)

            pointer = (pointer[0] + 1, pointer[1])

        return (int(''.join(values)), visited)


    def solve(self):
        start_time = time()

        self.parse_schematic()

        part_numbers = []
        part_num_positions = set()
        symbols = [key for key, value in self.schematic.items() if not value.isdigit()]
        for symbol_location in symbols:
            checked = set()
            for pos in self.adjacent(symbol_location):
                if pos in checked:
                    continue

                if pos in self.schematic and self.schematic[pos].isdigit():
                    number, visited = self.get_number(pos)
                    part_numbers.append(number)
                    checked = checked.union(visited)
                    part_num_positions = part_num_positions.union(visited)

        part1 = sum(part_numbers)

        gear_ratios = []
        gear_numbers = set()
        gear_symbols = [key for key, value in self.schematic.items() if value == GEAR]
        for gear_location in gear_symbols:
            checked = set()
            ratio_values = []
            for pos in self.adjacent(gear_location):
                if pos in checked:
                    continue

                if pos in self.schematic and self.schematic[pos].isdigit():
                    number, visited = self.get_number(pos)
                    ratio_values.append(number)
                    checked = checked.union(visited)

            if len(ratio_values) == 2:
                gear_ratios.append(ratio_values[0] * ratio_values[1])
                gear_numbers = gear_numbers.union(checked)

        part2 = sum(gear_ratios)

        end_time = time()
        seconds_elapsed = end_time - start_time

        data = {}
        for pos in self.schematic:
            if pos in gear_numbers:
                data[pos] = 'g' # gear number
            elif pos in part_num_positions:
                data[pos] = 'p' # part number
            elif self.schematic[pos] in '0123456789':
                data[pos] = 'n' # not a part number
            elif self.schematic[pos] in '*':
                data[pos] = '*' # gear
            elif self.schematic[pos] in '+-/@#$%&':
                data[pos] = 's' # symbol

        colors = {
            'n': (50, 50, 255),     # Not a part number is Blue 
            's': (200, 50, 50),     # Symbol is Red
            '*': (255, 255, 0),     # Gear symbol is Yellow
            'g': (50, 200, 50),     # Gear part number is Green
            'p': (255, 255, 255),   # Part number is White
        }

        self.image_map(data, colors, scale=5).save(self.visual_path('schematic.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
