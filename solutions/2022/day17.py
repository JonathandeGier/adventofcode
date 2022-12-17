from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

WALL = '#'

DOWN = 'v'
LEFT = '<'
RIGHT = '>'

DIRECTIONS = {
    DOWN: (0, -1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

class Shape:
    def __init__(self, id: int, units: list):
        self.id = id
        # unit positions relative to the bottom left corner
        self.units = units

    def intersects(self, position: tuple, map: set) -> bool:
        for pos in self.absolute_units(position):
            if pos in map:
                return True

            if pos[0] <= 0 or pos[0] >= 8: # intersecting with the wall
                return True
        return False

    def absolute_units(self, position: tuple) -> list:
        return [(pos[0] + position[0], pos[1] + position[1]) for pos in self.units]

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Pyroclastic Flow" # Tetris
        self.input = self.getInput(self.day)

        self.map = {}
        self.jetstream = []
        self.shapes = []

        self.make_video = False
        self.video = None

    def load_pattern(self):
        self.map = {}
        self.jetstream = [char for char in self.input.strip()]
        
        self.shapes = []
        self.shapes.append(Shape(0, [(0, 0), (1, 0), (2, 0), (3, 0)])) # -
        self.shapes.append(Shape(1, [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)])) # +
        self.shapes.append(Shape(2, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])) # _|
        self.shapes.append(Shape(3, [(0, 0), (0, 1), (0, 2), (0, 3)])) # |
        self.shapes.append(Shape(4, [(0, 0), (1, 0), (1, 1), (0, 1)])) # .

        # floor
        self.map[0, 0] = WALL
        self.map[1, 0] = WALL
        self.map[2, 0] = WALL
        self.map[3, 0] = WALL
        self.map[4, 0] = WALL
        self.map[5, 0] = WALL
        self.map[6, 0] = WALL
        self.map[7, 0] = WALL
        self.map[8, 0] = WALL

    def solve(self):
        start_time = time()

        self.load_pattern()
        
        current_jet = 0
        next_shape = 0
        placed_shapes = 0
        shape_location = None
        shape: Shape = None

        if self.make_video:
            img = self.image()
            self.video = cv2.VideoWriter(self.visual_path('tetris.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 15, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        save_state = False
        seen_states = {}
        while True:
            if shape is None:
                if save_state:
                    floor_heights = [max([pos[1] for pos in self.map.keys() if pos[0] == x]) for x in range(1, 8)]
                    max_wall = max(floor_heights)
                    min_wall = min(floor_heights)
                    
                    floor_state = [pos for pos in self.map if pos[1] >= min_wall and pos[1] <= max_wall]
                    floor_state = tuple([(pos[0], max_wall - pos[1]) for pos in floor_state])
                    
                    state = (current_jet % len(self.jetstream), next_shape % len(self.shapes), floor_state)
                    
                    if state not in seen_states:
                        seen_states[state] = (max_wall, placed_shapes)
                    else:
                        seen_state = seen_states[state]
                        old_max_wall = seen_state[0]
                        old_places_shapes = seen_state[1]
                        
                        max_wall_diff = max_wall - old_max_wall
                        places_shapes_diff = placed_shapes - old_places_shapes

                        target = 1_000_000_000_000 # 1 trillion
                        cycles = target // places_shapes_diff - 2

                        new_max_wall = max_wall + (max_wall_diff * cycles)
                        new_placed_shapes = placed_shapes + (places_shapes_diff * cycles)

                        # generate the floor state
                        for pos in floor_state:
                            self.map[pos[0], new_max_wall - pos[1]] = WALL

                        max_wall = new_max_wall
                        placed_shapes = new_placed_shapes
                        save_state = False

                max_wall = max([pos[1] for pos in self.map.keys()])
                shape = self.shapes[next_shape % len(self.shapes)]
                next_shape += 1

                shape_location = (3, max_wall + 4)

            if self.make_video and placed_shapes < 25:
                img = self.image(shape, shape_location)
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            # push by jetstream
            direction = self.jetstream[current_jet % len(self.jetstream)]
            current_jet += 1

            diff = DIRECTIONS[direction]
            new_location = (shape_location[0] + diff[0], shape_location[1] + diff[1])
            if not shape.intersects(new_location, self.map):
                shape_location = new_location

            if self.make_video and placed_shapes < 25:
                img = self.image(shape, shape_location)
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            # Move down
            diff = DIRECTIONS[DOWN]
            new_location = (shape_location[0] + diff[0], shape_location[1] + diff[1])
            if shape.intersects(new_location, self.map):
                # place the shape on the map in the current location
                for pos in shape.absolute_units(shape_location):
                    self.map[pos] = shape.id
                placed_shapes += 1
                shape = None
                shape_location = None
            else:
                shape_location = new_location

            if self.make_video and placed_shapes < 25:
                img = self.image(shape, shape_location)
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            if placed_shapes == 2022:
                part1 = max([pos[1] for pos in self.map.keys()])
                save_state = True
            
            if placed_shapes == 1_000_000_000_000:
                part2 = max([pos[1] for pos in self.map.keys()])
                break

        if self.make_video:
            img = self.image()
            for _ in range(75):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            self.video.release()
            img.save(self.visual_path('tetris.png'))
            cv2.destroyAllWindows()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, shape: Shape = None, shape_position: tuple = None):
        img = Image.new('RGB', (9, 31), 'black')
        pixels = img.load()

        def color_value(val):
            if val == WALL:
                return (100, 100, 100)
            elif val == 0:
                return (0, 255, 255)
            elif val == 1:
                return (128, 0, 128)
            elif val == 2:
                return (255, 127, 28)
            elif val == 3:
                return (0, 255, 0)
            elif val == 4:
                return (255, 255, 0)

        for pos in self.map:
            if 0<=pos[0]<9 and 0<=pos[1]<31:
                pixels[pos] = color_value(self.map[pos])

        if shape_position is not None and shape is not None:
            for pos in shape.absolute_units(shape_position):
                if 0<=pos[0]<9 and 0<=pos[1]<31:
                    pixels[pos] = color_value(shape.id)

        for y in range(31):
            pixels[0, y] = (100, 100, 100)
            pixels[8, y] = (100, 100, 100)

        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
