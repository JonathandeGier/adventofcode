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
            next_i = (i+1) % len(red_tiles)
            start, end = red_tiles[i], red_tiles[next_i]

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
    
    def line_in_shape(self, line_start, line_end, red_tiles):
        for i in range(len(red_tiles)):
            next_i = (i+1) % len(red_tiles)
            start, end = red_tiles[i], red_tiles[next_i]

            if line_start[0] == line_end[0]:
                # vertical line, search for crossing horizontal lines
                if start[1] == end[1] and min(start[0], end[0]) < line_start[0] and line_start[0] < max(start[0], end[0]) \
                    and min(line_start[1], line_end[1]) < start[1] and start[1] < max(line_start[1], line_end[1]):

                    return False
            elif line_start[1] == line_end[1]:
                # horizontal line, search for crossing vertical lines
                if start[0] == end[0] and min(start[1], end[1]) < line_start[1] and line_start[1] < max(start[1], end[1]) \
                    and min(line_start[0], line_end[0]) < start[0] and start[0] < max(line_start[0], line_end[0]):

                    return False
            else:
                assert False, 'Line on a diagonal'

        return True
    
    def no_red_tile_in_shape(self, corner1, corner2, red_tiles) -> bool:
        min_corner = (min(corner1[0], corner2[0]), min(corner1[1], corner2[1]))
        max_corner = (max(corner1[0], corner2[0]), max(corner1[1], corner2[1]))

        for tile in red_tiles:
            if min_corner[0] < tile[0] and tile[0] < max_corner[0] and min_corner[1] < tile[1] and tile[1] < max_corner[1]:
                return False
            
        return True


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

            # other 2 corners of the square
            other_1 = (start[0], end[1])
            other_2 = (end[0], start[1])

            # All edges of the square
            line1 = (start, other_1)
            line2 = (start, other_2)
            line3 = (end, other_1)
            line4 = (end, other_2)            

            if self.on_green_tile(other_1, tiles) and \
                self.on_green_tile(other_2, tiles) and \
                self.line_in_shape(line1[0], line1[1], tiles) and \
                self.line_in_shape(line2[0], line2[1], tiles) and \
                self.line_in_shape(line3[0], line3[1], tiles) and \
                self.line_in_shape(line4[0], line4[1], tiles) and \
                self.no_red_tile_in_shape(start, end, tiles):

                part2 = max(part2, area)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
