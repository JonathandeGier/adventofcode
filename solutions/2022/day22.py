from Table import Table
from time import time
from PIL import Image

WALL = '#'
OPEN = '.'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

NEW_DIRECTION = {
    UP: {
        LEFT: LEFT,
        RIGHT: RIGHT,
    },
    DOWN: {
        LEFT: RIGHT,
        RIGHT: LEFT,
    },
    LEFT: {
        LEFT: DOWN,
        RIGHT: UP,
    },
    RIGHT: {
        LEFT: UP,
        RIGHT: DOWN,
    },
}

DIRECTION_VALUES = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3,
}

SIZE = 50

FRONT = 'F'
BACK = 'B'

FACES = [FRONT, LEFT, RIGHT, UP, DOWN, BACK]

# current_face->direction: new_face, rotation
NEXT_FACE = {
    #       FRONT->UP = UP, no rotation
    #       FRONT->DOWN = DOWN, no rotation
    #       FRONT->LEFT = LEFT, no rotation
    #       FRONT->RIGHT = RIGHT, no rotation
    FRONT: {
        UP: (UP, 0),
        DOWN: (DOWN, 0),
        LEFT: (LEFT, 0),
        RIGHT: (RIGHT, 0),
    },
    #       LEFT->UP = UP, rotated counter-clockwise
    #       LEFT->DOWN = DOWN, rotated clockwise
    #       LEFT->LEFT = BACK, no rotation
    #       LEFT->RIGHT = FRONT, no rotation
    LEFT: {
        UP: (UP, 3),
        DOWN: (DOWN, 1),
        LEFT: (BACK, 0),
        RIGHT: (FRONT, 0),
    },
    #       RIGHT->UP = UP, rotated clockwise
    #       RIGHT->DOWN = DOWN, rotated counter-clockwise
    #       RIGHT->LEFT = FRONT, no rotation
    #       RIGHT->RIGHT = BACK, no rotation
    RIGHT: {
        UP: (UP, 1),
        DOWN: (DOWN, 3),
        LEFT: (FRONT, 0),
        RIGHT: (BACK, 0),
    },
    #       UP->UP = BACK, upside down
    #       UP->DOWN = FRONT, no rotation
    #       UP->LEFT = LEFT, rotated clockwise
    #       UP->RIGHT = RIGHT, rotated counter-clockwise
    UP: {
        UP: (BACK, 2),
        DOWN: (FRONT),
        LEFT: (LEFT, 1),
        RIGHT: (RIGHT, 2),
    },
    #       DOWN->UP = FRONT, no rotation
    #       DOWN->DOWN = BACK, upside down
    #       DOWN->LEFT = LEFT, rotated counter-clockwise
    #       DOWN->RIGHT = RIGHT, rotated clockwise
    DOWN: {
        UP: (FRONT, 0),
        DOWN: (BACK, 2),
        LEFT: (LEFT, 3),
        RIGHT: (RIGHT, 1),
    },
    #       BACK->UP = UP, upside down
    #       BACK->DOWN = DOWN, upside down
    #       BACK->LEFT = RIGHT, no rotation
    #       BACK->RIGHT = LEFT, no rotation
    BACK: {
        UP: (UP, 2),
        DOWN: (DOWN, 2),
        LEFT: (RIGHT, 0),
        RIGHT: (LEFT, 0),
    },
}


class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Monkey Map"
        self.input = self.getInput(self.day)

        self.map = {}
        self.directions = []

        self.make_image = False


    def load_map(self):
        self.map = {}
        for row, line in enumerate(self.input.splitlines()[:-2]):
            for col, val in enumerate(line):
                if val in [OPEN, WALL]:
                    self.map[row +1, col + 1] = val
        
        self.directions = []
        current = ''
        for val in self.input.splitlines()[-1]:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if len(current) > 0:
                    self.directions.append(int(current))
                    current = ''
                self.directions.append(val)
            else:
                current +=val

        if len(current) > 0:
            self.directions.append(int(current))

    def map_edges(self):
        # Identify where the faces are
        face_locations = []
        for row in range(4):
            for col in range(4):
                if (row * SIZE + 1, col * SIZE + 1) in self.map:
                    face_locations.append((row, col))
        assert len(face_locations) == 6

        first_face = face_locations[0]

        # face: face_row, face, col, face_rotation
        face_definitions = {
            FRONT: (first_face[0], first_face[1], 0),
            LEFT: None,
            RIGHT: None,
            UP: None,
            DOWN: None,
            BACK: None,
        }



        # 2: Take a face and call it FRONT
        # 3: BFS the other faces

        # 3.1. store these faces in a map -> FACE: x, y, rotation
        # 4. map edges -> (from_row, from_col, direction): (to_row, to_col, new_direction)


    def solve(self):
        start_time = time()

        self.load_map()

        col = min([coor[1] for coor in self.map if coor[0] == 1])
        position = (1, col)
        direction = 'R'

        visited = set()
        visited.add(position)

        for move in self.directions:
            if type(move) == int:
                for _ in range(move):
                    if direction == 'U':
                        next_pos = (position[0] - 1, position[1])
                    elif direction == 'D':
                        next_pos = (position[0] + 1, position[1])
                    elif direction == 'L':
                        next_pos = (position[0], position[1] - 1)
                    elif direction == 'R':
                        next_pos = (position[0], position[1] + 1)
                    else:
                        assert False

                    if next_pos not in self.map:
                        if direction == 'U':
                            next_pos = (max([coor[0] for coor in self.map if coor[1] == position[1]]), position[1])
                        elif direction == 'D':
                            next_pos = (min([coor[0] for coor in self.map if coor[1] == position[1]]), position[1])
                        elif direction == 'L':
                            next_pos = (position[0], max([coor[1] for coor in self.map if coor[0] == position[0]]))
                        elif direction == 'R':
                            next_pos = (position[0], min([coor[1] for coor in self.map if coor[0] == position[0]]))
                        else:
                            assert False

                    assert next_pos in self.map

                    if self.map[next_pos] == OPEN:
                        position = next_pos
                    elif self.map[next_pos] == WALL:
                        break
                    else:
                        assert False

                    visited.add(position)
            else:
                direction = NEW_DIRECTION[direction][move]

            # print(position)
            

        part1 = (1000 * position[0]) + (4 * position[1]) + DIRECTION_VALUES[direction]
        
        if self.make_image:
            self.image().save(self.visual_path('map.png'))
            self.image(visited).save(self.visual_path('path.png'))
        

        part2 = "None"
        self.map_edges()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, visited = set()):
        max_row = max([coor[0] for coor in self.map])
        max_col = max([coor[1] for coor in self.map])
        img = Image.new('RGB', (max_col, max_row), 'black')
        pixels = img.load()
        for pos in self.map:
            if self.map[pos] == OPEN:
                color = (100, 100, 100)
            elif self.map[pos] == WALL:
                color = (255, 255, 255)
            else:
                color = (255, 0, 0)

            pixels[pos[1] - 1, pos[0] - 1] = color

        for pos in visited:
            pixels[pos[1] - 1, pos[0] - 1] = (255, 0, 0)

        return img


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
