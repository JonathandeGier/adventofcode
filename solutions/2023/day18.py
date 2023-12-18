from Table import Table
from time import time
from collections import deque

DIRECTION = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "Lavaduct Lagoon"
        self.input = self.getInput(self.day)

        self.vertices = []
        self.border = 0
        self.big_vertices = []
        self.big_border = 0

        self.make_image = False and __name__ == '__main__'

    def move(self, pos: tuple, dir: str, length: int = 1) -> tuple:
        if dir == 'U':
            return (pos[0], pos[1] - length)
        elif dir == 'D':
            return (pos[0], pos[1] + length)
        elif dir == 'L':
            return (pos[0] - length, pos[1])
        elif dir == 'R':
            return (pos[0] + length, pos[1])
        else:
            assert False, f'Unknown direction {dir}'

    def parse_dig_plan(self):        
        self.vertices = []
        self.border = 0
        
        self.big_vertices = []
        self.big_border = 0

        pos1 = (0, 0)
        pos2 = (0, 0)
        for line in self.input.splitlines():
            dir1, distance1, color = line.split(' ')

            pos1 = self.move(pos1, dir1, int(distance1))
            self.vertices.append(pos1)
            self.border += int(distance1)
            
            distance2 = int(color[2:-2], base=16)
            dir2 = DIRECTION[color[-2:-1]]

            pos2 = self.move(pos2, dir2, distance2)
            self.big_vertices.append(pos2)
            self.big_border += distance2


    def calculate_area(self, vertices: list, border: int) -> int:
        # Shoelace formula (Trapezoid): https://en.wikipedia.org/wiki/Shoelace_formula 
        sum = 0
        for i in range(len(vertices) - 1):
            sum += ((vertices[i][0] - vertices[i+1][0]) * (vertices[i][1] + vertices[i+1][1]))

        return sum // 2 + (border // 2) + 1
        

    def image_data(self, part2: bool = False):
        data = {}
        pos = (0, 0)

        # parse input
        for line in self.input.splitlines():
            dir1, distance, color = line.split(' ')

            if part2:
                distance2 = int(color[2:-2], base=16) // 10000
                dir2 = DIRECTION[color[-2:-1]]
                for _ in range(distance2):
                    pos = self.move(pos, dir2)
                    data[pos] = '#'

            else:
                for _ in range(int(distance)):
                    pos = self.move(pos, dir1)
                    data[pos] = '#'

        if part2:
            # closes the area since we loose accuracy bey dividing by 10000
            # also likely only works for my input
            data[(0, 0)] = '#'
            data[(1, 0)] = '#'
            data[(2, 0)] = '#'
            data[(3, 0)] = '#'
            data[(4, 0)] = '#'
            data[(5, 0)] = '#'
            data[(6, 0)] = '#'
            data[(7, 0)] = '#'
            data[(8, 0)] = '#'
            data[(9, 0)] = '#'
            data[(10, 0)] = '#'
            data[(10, 1)] = '#'
        
        # bfs inside
        queue = deque()
        if part2:
            queue.append((1, -1))
        else:
            queue.append((1, 1))

        while queue:
            pos = queue.popleft()

            if pos in data:
                continue

            data[pos] = 'L' # Lava

            for dir in DIRECTION.values():
                new_pos = self.move(pos, dir)

                if new_pos not in data:
                    queue.append(new_pos)

        return data

    def solve(self):
        start_time = time()

        self.parse_dig_plan()

        part1 = self.calculate_area(self.vertices, self.border)
        part2 = self.calculate_area(self.big_vertices, self.big_border)

        if self.make_image:
            data = self.image_data()
            self.image_map(data, {'#': (200, 200, 200)}, padding=2).save(self.visual_path('bounds1.png'))
            self.image_map(data, {'#': (200, 200, 200), 'L': (235, 60, 23)}, padding=2).save(self.visual_path('filled1.png'))

            data = self.image_data(True)
            self.image_map(data, {'#': (200, 200, 200)}, padding=2).save(self.visual_path('bounds2.png'))
            self.image_map(data, {'#': (200, 200, 200), 'L': (235, 60, 23)}, padding=2).save(self.visual_path('filled2.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
