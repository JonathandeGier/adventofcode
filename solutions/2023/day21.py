from Table import Table
from time import time

from PIL import Image

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Step Counter"
        self.input = self.getInput(self.day)

        self.map = {}
        self.side_length = 0

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = val
        max_x = x
        max_y = y

        assert max_x == max_y, 'This code assumes a square map'
        assert max_x % 2 == 0, f'This code assumes a uneven side length {max_x}'

        self.side_length = max_x + 1

    def possible_places(self, start: tuple, steps: int) -> int:
        possible_places = set([start])
        for _ in range(steps):
            new_places = set()
            for place in possible_places:
                for dir in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    new_place = (place[0] + dir[0], place[1] + dir[1])
                    if new_place not in self.map or self.map[new_place] == '#':
                        continue

                    new_places.add(new_place)

            possible_places = new_places
        
        return possible_places

    def solve(self):
        start_time = time()

        self.parse_map()

        start = [pos for pos in self.map if self.map[pos] == 'S'][0]
        assert start == (self.side_length // 2, self.side_length // 2), 'This code assumes the start point is the center of the map'

        part1_possible_places = self.possible_places(start, 64)
        part1 = len(part1_possible_places)

        self.image_map(self.map, {'#': (255, 255, 255)}, scale=5).save(self.visual_path('map.png'))
        self.possible_places_image(part1_possible_places, scale=5).save(self.visual_path('part1.png'))

        # More assumptions, which due to map layout may not be true:
        # from center to edge is side_length // 2 steps
        # from edge to edge is side_length steps
        # to fill the square including the start point takes side_length - 1 steps
        # to fill the square excluding the start point takes side_length - 2 steps

        # Steps from the center generates this pattern, where each #, O, <, >, ^, V, /, /, \, and \ is the same instance of the map with generated steps
        #    .^.
        #   ./O\.
        #  ./O#O\.
        # ./O#O#O\.
        # <O#O#O#O>
        # .\O#O#O/.
        #  .\O#O/.
        #   .\O/.
        #    .V.

        steps = 26501365
        edge_filled_squares = (steps - (self.side_length // 2)) // self.side_length
        assert (steps - (self.side_length // 2)) % self.side_length == 0, 'This code assumes the corner patterns touches the end'

        # calculate the number of different types of squares
        center_squares = (edge_filled_squares - 1) ** 2
        outer_squares = (edge_filled_squares) ** 2

        inner_corner_squares = edge_filled_squares - 1
        outer_corner_squares = edge_filled_squares

        # calculate the possible places for each unique square
        center_square_available_places = self.possible_places(start, self.side_length)
        outer_square_available_places = self.possible_places(start, self.side_length - 1)

        left_possible_places = self.possible_places((self.side_length, self.side_length // 2), self.side_length)
        top_left_inner_possible_places = self.possible_places((self.side_length - 1, self.side_length - 1), (self.side_length + self.side_length // 2) - 1)
        top_left_outer_possible_places = self.possible_places((self.side_length - 1, self.side_length - 1), (self.side_length // 2) - 1)

        top_possible_places = self.possible_places((self.side_length // 2, self.side_length), self.side_length)
        top_right_inner_possible_places = self.possible_places((0, self.side_length - 1), (self.side_length + self.side_length // 2) - 1)
        top_right_outer_possible_places = self.possible_places((0, self.side_length - 1), (self.side_length // 2) - 1)

        right_possible_places = self.possible_places((0, self.side_length // 2), self.side_length - 1)
        right_bottom_inner_possible_places = self.possible_places((0, 0), (self.side_length + self.side_length // 2) - 1)
        right_bottom_outer_possible_places = self.possible_places((0, 0), (self.side_length // 2) - 1)

        bottom_possible_places = self.possible_places((self.side_length // 2, 0), self.side_length - 1)
        bottom_left_inner_possible_places = self.possible_places((self.side_length - 1, 0), (self.side_length + self.side_length // 2) - 1)
        bottom_left_outer_possible_places = self.possible_places((self.side_length - 1, 0), (self.side_length // 2) - 1)

        # sum them all up
        part2 = sum([
            center_squares * len(center_square_available_places),
            outer_squares * len(outer_square_available_places),

            1 * len(left_possible_places),
            inner_corner_squares * len(top_left_inner_possible_places),
            outer_corner_squares * len(top_left_outer_possible_places),

            1 * len(top_possible_places),
            inner_corner_squares * len(top_right_inner_possible_places),
            outer_corner_squares * len(top_right_outer_possible_places),

            1 * len(right_possible_places),
            inner_corner_squares * len(right_bottom_inner_possible_places),
            outer_corner_squares * len(right_bottom_outer_possible_places),

            1 * len(bottom_possible_places),
            inner_corner_squares * len(bottom_left_inner_possible_places),
            outer_corner_squares * len(bottom_left_outer_possible_places),
        ])

        end_time = time()
        seconds_elapsed = end_time - start_time

        # images
        self.expanded_image(self.map, {'#': (255, 255, 255)}, repeat=5).save(self.visual_path('expanded.png'))

        self.possible_places_image(center_square_available_places).save(self.visual_path('pieces/center_square_available_places.png'))
        self.possible_places_image(outer_square_available_places).save(self.visual_path('pieces/outer_square_available_places.png'))
        self.possible_places_image(left_possible_places).save(self.visual_path('pieces/left_possible_places.png'))
        self.possible_places_image(top_left_inner_possible_places).save(self.visual_path('pieces/top_left_inner_possible_places.png'))
        self.possible_places_image(top_left_outer_possible_places).save(self.visual_path('pieces/top_left_outer_possible_places.png'))
        self.possible_places_image(top_possible_places).save(self.visual_path('pieces/top_possible_places.png'))
        self.possible_places_image(top_right_inner_possible_places).save(self.visual_path('pieces/top_right_inner_possible_places.png'))
        self.possible_places_image(top_right_outer_possible_places).save(self.visual_path('pieces/top_right_outer_possible_places.png'))
        self.possible_places_image(right_possible_places).save(self.visual_path('pieces/right_possible_places.png'))
        self.possible_places_image(right_bottom_inner_possible_places).save(self.visual_path('pieces/right_bottom_inner_possible_places.png'))
        self.possible_places_image(right_bottom_outer_possible_places).save(self.visual_path('pieces/right_bottom_outer_possible_places.png'))
        self.possible_places_image(bottom_possible_places).save(self.visual_path('pieces/bottom_possible_places.png'))
        self.possible_places_image(bottom_left_inner_possible_places).save(self.visual_path('pieces/bottom_left_inner_possible_places.png'))
        self.possible_places_image(bottom_left_outer_possible_places).save(self.visual_path('pieces/bottom_left_outer_possible_places.png'))
        self.possible_places_image(set()).save(self.visual_path('pieces/empty.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def possible_places_image(self, possible_places: set, scale: int = 1):
        data = {pos:val for pos, val in self.map.items()}
        for pos in possible_places:
            data[pos] = 'O'
        return self.image_map(data, {'#': (255, 255, 255), 'O': (50, 50, 200)}, scale=scale)

    def expanded_image(self, data: map, colors: map, bounds: tuple = None, scale: int = 1, repeat: int = 1):
        if bounds is None:
            bounds = self.bounds(data)

        len_x = bounds[1] - bounds[0] + 1
        len_y = bounds[3] - bounds[2] + 1
        img = Image.new('RGB', (len_x * repeat, len_y * repeat), 'black')
        pixels = img.load()
        for position in data:
            if data[position] in colors:
                pixel = position[0] - bounds[0], position[1] - bounds[2]

                for repeat_x in range(repeat):
                    for repeat_y in range(repeat):
                        pixels[pixel[0] + repeat_x * len_x, pixel[1] + repeat_y * len_y] = colors[data[position]]

        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)
        return img

if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
