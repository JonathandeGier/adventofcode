from Table import Table
from time import time
from itertools import combinations

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Movie Theater"
        self.input = self.getInput(self.day)

    
    def on_green_tile(self, point, red_tiles) -> bool:
        # Point is a red tile
        if len([tile for tile in red_tiles if tile == point]) == 1:
            return True
        
        pairs = []
        for i in range(len(red_tiles)):
            next_i = i+1
            if next_i == len(red_tiles):
                i = 0

            start, end = red_tiles[i], red_tiles[i+1]

            # Point is on a line between red tiles
            if start[0] == point[0] and end[0] == point[0]:
                # on same x (vertical)
                if min(start[1], end[1]) <= point[1] and max(start[1], end[1]) >= point[1]:
                    return True
            elif start[1] == point[1] and end[1] == point[1]:
                # on same y (horizontal)
                if min(start[0], end[0]) <= point[0] and max(start[0], end[0]) >= point[0]:
                    return True
                
            # vertical line segment (same x)
            # to the left of the point
            # in the correct y segment
            if start[0] == end[0] and \
                start[0] < point[0] and \
                min(start[1], end[1]) <= point[1] and point[1] < max(start[1], end[1]):

                pairs.append((start, end))

        return len(pairs) % 2 == 1
    
    def line_in_shape(self, start, end, red_tiles):
        if start[0] == end[0]:
            # vertical line, search for crossing horizontal lines
            pass
        elif start[1] == end[1]:
            # horizontal line, search for crossing vertical lines
            pass
        else:
            assert False, 'Line on a diagonal'


    def solve(self):
        start_time = time()

        tiles = []
        for line in self.input.splitlines():
            x, y = line.split(',')
            tiles.append((int(x), int(y)))

        part1 = 0
        part2 = 0
        for start, end in combinations(tiles, 2):
            area = (abs(end[0] - start[0]) + 1) * (abs(end[1] - start[1]) + 1)
            part1 = max(part1, area)

            other_1 = (start[0], end[1])
            other_2 = (end[0], start[1])

            # if start == (11, 1) and end == (2, 5):
            #     print(other_1, other_2)
            #     print(self.on_line(other_1, tiles), self.in_shape(other_1, tiles))
            #     print(self.on_line(other_2, tiles), self.in_shape(other_2, tiles))
            #     print((self.on_line(other_1, tiles) or self.in_shape(other_1, tiles)) and (self.on_line(other_2, tiles) or self.in_shape(other_2, tiles)))


            if self.on_green_tile(other_1, tiles) and self.on_green_tile(other_2, tiles):
                # part2 = max(part2, area)
                if area > part2:
                    part2 = area
                    print(start, end, area)


        # ... < x < 4591195600
        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
