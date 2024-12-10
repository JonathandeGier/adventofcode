from Table import Table
from time import time

COLORS = {
    'X':(255, 0, 0),
    'M':(0, 255, 0),
    'A':(255, 255, 0),
    'S':(255, 0, 255),
}

COL = {
    0: 'X',
    1: 'M',
    2: 'A',
    3: 'S',
}

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Ceres Search"
        self.input = self.getInput(self.day)

        self.grid = None
        self.words = {}
        self.crosses = {}

    def parse_grid(self):
        self.grid = []
        for line in self.input.splitlines():
            row = []
            for val in line:
                row.append(val)
            self.grid.append(row)
    
    def in_grid(self, row, col) -> bool:
        return row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[0])
    
    def xmas_count(self, row, col) -> int:
        if self.grid[row][col] != 'X':
            return 0
        
        dirs = [
            {(0, 0): 'X', ( 0,  1): 'M', ( 0,  2): 'A', ( 0,  3): 'S'},
            {(0, 0): 'X', ( 0, -1): 'M', ( 0, -2): 'A', ( 0, -3): 'S'},
            {(0, 0): 'X', ( 1,  0): 'M', ( 2,  0): 'A', ( 3,  0): 'S'},
            {(0, 0): 'X', (-1,  0): 'M', (-2,  0): 'A', (-3,  0): 'S'},
            {(0, 0): 'X', ( 1,  1): 'M', ( 2,  2): 'A', ( 3,  3): 'S'},
            {(0, 0): 'X', ( 1, -1): 'M', ( 2, -2): 'A', ( 3, -3): 'S'},
            {(0, 0): 'X', (-1,  1): 'M', (-2,  2): 'A', (-3,  3): 'S'},
            {(0, 0): 'X', (-1, -1): 'M', (-2, -2): 'A', (-3, -3): 'S'},
        ]

        count = 0
        for i, dir in enumerate(dirs):
            valid = True
            for key in dir.keys():
                new_row = row + key[0]
                new_col = col + key[1]
                if not (self.in_grid(new_row, new_col) and self.grid[new_row][new_col] == dir[key]):
                    valid = False

            if valid:
                for key in dir.keys():
                    new_row = row + key[0]
                    new_col = col + key[1]
                    color = i % 4

                    self.words[new_col, new_row] = COL[color]
                count += 1
        
        return count
    
    def is_x_mas(self, row, col) -> bool:
        if self.grid[row][col] != 'A':
            return False
        
        tlbr1 = self.grid[row - 1][col - 1] == 'M' and self.grid[row + 1][col + 1] == 'S'
        tlbr2 = self.grid[row - 1][col - 1] == 'S' and self.grid[row + 1][col + 1] == 'M'
        trbl1 = self.grid[row - 1][col + 1] == 'M' and self.grid[row + 1][col - 1] == 'S'
        trbl2 = self.grid[row - 1][col + 1] == 'S' and self.grid[row + 1][col - 1] == 'M'

        valid = (tlbr1 or tlbr2) and (trbl1 or trbl2)

        if valid:
            for pos in ((0, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                if tlbr1 and trbl1:
                    color = 'X'
                elif tlbr1 and trbl2:
                    color = 'M'
                elif tlbr2 and trbl1:
                    color = 'A'
                else:
                    color = 'S'
                self.crosses[col + pos[1], row + pos[0]] = color

        return valid


    def solve(self):
        start_time = time()

        self.parse_grid()

        part1 = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                part1 += self.xmas_count(row, col)

        part2 = 0
        for row in range(1, len(self.grid) - 1):
            for col in range(1, len(self.grid[0]) - 1):
                if self.is_x_mas(row, col):
                    part2 += 1

        end_time = time()
        seconds_elapsed = end_time - start_time
        
        if __name__ == '__main__':
            self.image_map(self.words, COLORS, scale=5).save(self.visual_path('words.png'))
            self.image_map(self.crosses, COLORS, scale=5).save(self.visual_path('crosses.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
