from Table import Table
from time import time

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Parabolic Reflector Dish"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == '.':
                    continue
                self.map[(x, y)] = val
        
        self.max_x = max([pos[0] for pos in self.map.keys()])
        self.max_y = max([pos[1] for pos in self.map.keys()])

    def move_north(self):
        stones = sorted([pos for pos in self.map if self.map[pos] == 'O'], key=lambda pos: (pos[1], pos[0]))
        for stone in stones:
            if stone[1] == 0:
                continue

            new_y = stone[1]
            for y in range(stone[1] - 1, -1, -1):
                if (stone[0], y) not in self.map:
                    new_y = y
                else:
                    break

            del self.map[stone]
            self.map[(stone[0], new_y)] = 'O'

    def move_south(self):
        stones = sorted([pos for pos in self.map if self.map[pos] == 'O'], key=lambda pos: (pos[1], pos[0]), reverse=True)
        for stone in stones:
            if stone[1] == self.max_y:
                continue

            new_y = stone[1]
            for y in range(stone[1] + 1, self.max_y + 1):
                if (stone[0], y) not in self.map:
                    new_y = y
                else:
                    break

            del self.map[stone]
            self.map[(stone[0], new_y)] = 'O'

    def move_west(self):
        stones = sorted([pos for pos in self.map if self.map[pos] == 'O'], key=lambda pos: pos)
        for stone in stones:
            if stone[0] == 0:
                continue

            new_x = stone[0]
            for x in range(stone[0] - 1, -1, -1):
                if (x, stone[1]) not in self.map:
                    new_x = x
                else:
                    break

            del self.map[stone]
            self.map[(new_x, stone[1])] = 'O'

    def move_east(self):
        stones = sorted([pos for pos in self.map if self.map[pos] == 'O'], key=lambda pos: pos, reverse=True)
        for stone in stones:
            if stone[0] == self.max_x:
                continue

            new_x = stone[0]
            for x in range(stone[0] + 1, self.max_x + 1):
                if (x, stone[1]) not in self.map:
                    new_x = x
                else:
                    break
            
            del self.map[stone]
            self.map[(new_x, stone[1])] = 'O'

    def cycle(self, rounds: int):
        for i in range(rounds):
            self.move_north()
            self.move_west()
            self.move_south()
            self.move_east()


    def solve(self):
        start_time = time()

        self.parse_map()
        self.move_north()
        part1 = sum([self.max_y - pos[1] + 1 for pos in self.map if self.map[pos] == 'O'])


        self.parse_map()
        self.print_map('Start')
        self.cycle(1)
        self.print_map('After 1 cycle')
        self.cycle(1)
        self.print_map('After 2 cycles')
        self.cycle(1)
        self.print_map('After 3 cycles')
        self.cycle(1)
        self.print_map('After 4 cycles')

        i = 1_000_000_000
        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def print_map(self, title: str = ''):
        max_x = max([pos[0] for pos in self.map.keys()])
        max_y = max([pos[1] for pos in self.map.keys()])

        if title != '':
            print(title)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if (x, y) in self.map:
                    print(self.map[(x, y)], end='')
                else:
                    print('.', end='')
            print('')
        print('')


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
