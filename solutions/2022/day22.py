from Table import Table
from time import time
from PIL import Image
from collections import deque
import cv2
from numpy import asarray

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
        DOWN: (FRONT, 0),
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

ROTATE = {
    UP: {
        0: UP,
        1: RIGHT,
        2: DOWN,
        3: LEFT
    },
    DOWN: {
        0: DOWN,
        1: LEFT,
        2: UP,
        3: RIGHT,
    },
    LEFT: {
        0: LEFT,
        1: UP,
        2: RIGHT,
        3: DOWN,
    },
    RIGHT: {
        0: RIGHT,
        1: DOWN,
        2: LEFT,
        3: UP,
    },
}


class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Monkey Map"
        self.input = self.getInput(self.day)

        self.map = {}
        self.directions = []
        self.edge_mapping = {}

        self.face_maps = {
            FRONT: None,
            LEFT: None,
            RIGHT: None,
            UP: None,
            DOWN: None,
            BACK: None,
        }

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
        # manually map example edges
        # map edges -> (from_row, from_col, direction): (to_row, to_col, new_direction)
        self.edge_mapping = {}
        # for i in range(SIZE):
        #     # top clockwise to top anti-clockwisw
        #     from_row = 0 * SIZE + 1
        #     from_col = 2 * SIZE + i + 1
        #     to_row = 1 * SIZE + 1
        #     to_col = 0 * SIZE + SIZE - i
        #     self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, DOWN)

        #     # right clockwise to right anti-clockwise
        #     from_row = 0 * SIZE + 1 + i
        #     from_col = 2 * SIZE + SIZE
        #     to_row = 2 * SIZE + SIZE - i
        #     to_col = 3 * SIZE + SIZE
        #     self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, LEFT)

        #     # right clockwise to top anti-clockwise
        #     from_row = 1 * SIZE + 1 + i
        #     from_col = 2 * SIZE + SIZE
        #     to_row = 2 * SIZE + 1
        #     to_col = 3 * SIZE + SIZE - i
        #     self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, DOWN)

        #     # top clockwise to right anti clockwise
        #     from_row = 2 * SIZE + 1
        #     from_col = 3 * SIZE + 1 + i
        #     to_row = 1 * SIZE + SIZE - i
        #     to_col = 2 * SIZE + SIZE
        #     self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, LEFT)

        #     # right clockwise to right anti-clockwise
        #     from_row = 2 * SIZE + 1 + i
        #     from_col = 3 * SIZE + SIZE
        #     to_row = 0 * SIZE + SIZE - 1
        #     to_col = 2 * SIZE + SIZE
        #     self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, LEFT)

        #     # bottom clockwise to left anti-clockwise
        #     from_row = 2 * SIZE + SIZE
        #     from_col = 3 * SIZE + SIZE - i
        #     to_row = 1 * SIZE + i + 1
        #     to_col = 0 * SIZE + 1
        #     self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, RIGHT)

        #     # bottom clockwise to bottom anti-clockwise
        #     from_row = 2 * SIZE + SIZE
        #     from_col = 2 * SIZE + SIZE - i
        #     to_row = 1 * SIZE + SIZE
        #     to_col = 0 * SIZE + i + 1
        #     self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, UP)

        #     # left clockwise to bottom anti-clockwise
        #     from_row = 2 * SIZE + SIZE - i
        #     from_col = 2 * SIZE + 1
        #     to_row = 1 * SIZE + SIZE
        #     to_col = 1 * SIZE + i + 1
        #     self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, UP)

        #     # bottom clockwise to left anti clockwise
        #     from_row = 1 * SIZE + SIZE
        #     from_col = 1 * SIZE + SIZE - i
        #     to_row = 2 * SIZE + i + 1
        #     to_col = 2 * SIZE + 1
        #     self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, RIGHT)

        #     # bottom clockwise to bottom anti clockwise
        #     from_row = 1 * SIZE + SIZE
        #     from_col = 0 * SIZE + SIZE - i
        #     to_row = 2 * SIZE + SIZE
        #     to_col = 2 * SIZE + i + 1
        #     self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, UP)

        #     # left clockwise to bottom anti clockwise
        #     from_row = 1 * SIZE + SIZE - i
        #     from_col = 0 * SIZE + 1
        #     to_row = 2 * SIZE + SIZE
        #     to_col = 3 * SIZE + i + 1
        #     self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, UP)

        #     # up clockwise to up anti-clockwise
        #     from_row = 1 * SIZE + 1
        #     from_col = 0 * SIZE + i + 1
        #     to_row = 0 * SIZE + 1
        #     to_col = 2 * SIZE + SIZE - i
        #     self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, DOWN)

        #     # up clockwise to left anti-clockwise
        #     from_row = 1 * SIZE + 1
        #     from_col = 1 * SIZE + i + 1
        #     to_row = 0 * SIZE + i + 1
        #     to_col = 2 * SIZE + 1
        #     self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, RIGHT)

        #     # left clockwise to up anti-clockwise
        #     from_row = 0 * SIZE + SIZE - i
        #     from_col = 2 * SIZE + 1
        #     to_row = 1 * SIZE + 1
        #     to_col = 1 * SIZE + SIZE - i
        #     self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, DOWN)

        # manually map input edges
        # Top edge:
        #     clockwise:
        #     row = face_definitions[face][0] * SIZE + 1
        #     col = face_definitions[face][1] * SIZE + i + 1
        # 
        #     anti-clockwise:
        #     row = face_definitions[face][0] * SIZE + 1
        #     col = face_definitions[face][1] * SIZE + SIZE - i 
        # right edge:
        #     clockwise:
        #     row = face_definitions[face][0] * SIZE + i + 1
        #     col = face_definitions[face][1] * SIZE + SIZE
        # 
        #     anti-clockwise:
        #     row = face_definitions[face][0] * SIZE + SIZE - i
        #     col = face_definitions[face][1] * SIZE + SIZE
        # bottom edge:
        #     clockwise:
        #     row = face_definitions[face][0] * SIZE + SIZE
        #     col = face_definitions[face][1] * SIZE + SIZE - i
        # 
        #     anti-clockwise:
        #     row = face_definitions[face][0] * SIZE + SIZE
        #     col = face_definitions[face][1] * SIZE + i + 1
        # left edge:
        #     clockwise:
        #     row = face_definitions[face][0] * SIZE + SIZE - i
        #     col = face_definitions[face][1] * SIZE + 1
        # 
        #     anti-clockwise:
        #     row = face_definitions[face][0] * SIZE + i + 1
        #     col = face_definitions[face][1] * SIZE + 1
        for i in range(SIZE):
            # top clockwise tp left anti-clockwise
            from_row = 0 * SIZE + 1
            from_col = 1 * SIZE + i + 1
            to_row = 3 * SIZE + i + 1
            to_col = 0 * SIZE + 1
            self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, RIGHT)

            # top clockwise to bottom anti-clockwise
            from_row = 0 * SIZE + 1
            from_col = 2 * SIZE + i + 1
            to_row = 3 * SIZE + SIZE
            to_col = 0 * SIZE + i + 1
            self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, UP)

            # right clockwise to right anti-clockwise
            from_row = 0 * SIZE + i + 1
            from_col = 2 * SIZE + SIZE
            to_row = 2 * SIZE + SIZE - i
            to_col = 1 * SIZE + SIZE
            self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, LEFT)

            # Bottom clockwise to right anti-clockwise
            from_row = 0 * SIZE + SIZE
            from_col = 2 * SIZE + SIZE - i
            to_row = 1 * SIZE + SIZE - i
            to_col = 1 * SIZE + SIZE
            self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, LEFT)

            # right-clockwise to bottom anti-clockwise
            from_row = 1 * SIZE + i + 1
            from_col = 1 * SIZE + SIZE
            to_row = 0 * SIZE + SIZE
            to_col = 2 * SIZE + i + 1
            self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, UP)

            # right clockwise to right anti-clockwise
            from_row = 2 * SIZE + i + 1
            from_col = 1 * SIZE + SIZE
            to_row = 0 * SIZE + SIZE - i
            to_col = 2 * SIZE + SIZE
            self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, LEFT)

            # Bottom clockwise to right anti-clockwise
            from_row = 2 * SIZE + SIZE
            from_col = 1 * SIZE + SIZE - i
            to_row = 3 * SIZE + SIZE - i
            to_col = 0 * SIZE + SIZE
            self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, LEFT)

            # right-clockwise to bottom anti-clockwise
            from_row = 3 * SIZE + i + 1
            from_col = 0 * SIZE + SIZE
            to_row = 2 * SIZE + SIZE
            to_col = 1 * SIZE + i + 1
            self.edge_mapping[(from_row, from_col, RIGHT)] = (to_row, to_col, UP)

            # bottom clockwise to top anti-clockwise
            from_row = 3 * SIZE + SIZE
            from_col = 0 * SIZE + SIZE - i
            to_row = 0 * SIZE + 1
            to_col = 2 * SIZE + SIZE - i
            self.edge_mapping[(from_row, from_col, DOWN)] = (to_row, to_col, DOWN)

            # left clockwise to top anti-clockwise
            from_row = 3 * SIZE + SIZE - i
            from_col = 0 * SIZE + 1
            to_row = 0 * SIZE + 1
            to_col = 1 * SIZE + SIZE - i
            self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, DOWN)

            # left clockwise to left anti-clockwise
            from_row = 2 * SIZE + SIZE - i
            from_col = 0 * SIZE + 1
            to_row = 0 * SIZE + i + 1
            to_col = 1 * SIZE + 1
            self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, RIGHT)

            # top clockwise to left anti-clockwise
            from_row = 2 * SIZE + 1
            from_col = 0 * SIZE + i + 1
            to_row = 1 * SIZE + i + 1
            to_col = 1 * SIZE + 1
            self.edge_mapping[(from_row, from_col, UP)] = (to_row, to_col, RIGHT)

            # left clockwise to top anti-clockwise
            from_row = 1 * SIZE + SIZE - i
            from_col = 1 * SIZE + 1
            to_row = 2 * SIZE + 1
            to_col = 0 * SIZE + SIZE - i
            self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, DOWN)

            # left clockwise to left anti-clockwise
            from_row = 0 * SIZE + SIZE - i
            from_col = 1 * SIZE + 1
            to_row = 2 * SIZE + i + 1
            to_col = 0 * SIZE + 1
            self.edge_mapping[(from_row, from_col, LEFT)] = (to_row, to_col, RIGHT)

        return

        # Identify where the faces are
        face_locations = {}
        for row in range(4):
            for col in range(4):
                if (row * SIZE + 1, col * SIZE + 1) in self.map:
                    face_locations[(row, col)] = None
        assert len(face_locations) == 6

        first_face = list(face_locations.keys())[0]
        face_locations[first_face] = FRONT

        # face: face_row, face, col, face_rotation
        face_definitions = {
            FRONT: (first_face[0], first_face[1], 0),
            LEFT: None,
            RIGHT: None,
            UP: None,
            DOWN: None,
            BACK: None,
        }

        # 3: BFS the other faces to get all face definitions
        queue = deque([first_face])
        while len(queue) > 0:
            face_location = queue.popleft()
            current_face = face_locations[face_location]

            for direction in [(-1, 0, UP), (1, 0, DOWN), (0, -1, LEFT), (0, 1, RIGHT)]:
                new_location = (face_location[0] + direction[0], face_location[1] + direction[1])
                if new_location not in face_locations:
                    continue

                new_direction = ROTATE[direction[2]][face_definitions[current_face][2]]
                new_face = NEXT_FACE[current_face][new_direction]
                if face_definitions[new_face[0]] is not None:
                    continue

                face_definitions[new_face[0]] = (new_location[0], new_location[1], (face_definitions[current_face][2] + new_face[1]) % 4)
                face_locations[new_location] = new_face[0]

                queue.append(new_location)

        face_definitions[UP] = (1, 0, 2)
        print(face_definitions)

        rot_edge = {
            0: UP,
            1: RIGHT,
            2: DOWN,
            3: LEFT,
        }


        # 4. get edge coordinates
        # edge_coords = {}
        # for face in FACES:
        #     edge_coords[face] = {}
        #     for edge in [0, 1, 2, 3]:
        #         edge_coords[face][edge] = {}
        #         face_edge = (face_rotation + edge) % 4

        #         for i in range(SIZE):
        #             if face_edge == 0:
        #                 from_row = face_definitions[face][0] * SIZE + 1
        #                 from_col = face_definitions[face][1] * SIZE + i + 1
        #             elif face_edge == 1:
        #                 from_row = face_definitions[face][0] * SIZE + i + 1
        #                 from_col = face_definitions[face][1] * SIZE + SIZE
        #             elif face_edge == 2:
        #                 from_row = face_definitions[face][0] * SIZE + SIZE
        #                 from_col = face_definitions[face][1] * SIZE + SIZE - i
        #             elif face_edge == 3:
        #                 from_row = face_definitions[face][0] * SIZE + SIZE - i
        #                 from_col = face_definitions[face][1] * SIZE + 1
        #             else:
        #                 assert False

        #             edge_coords[face][edge][i] = (from_row, from_col)

            # face_map_positions = [(row, col) for row, col in self.map if row > face_definitions[face][0] * SIZE and row <= face_definitions[face][0] * SIZE + SIZE and col > face_definitions[face][1] * SIZE and col <= face_definitions[face][1] * SIZE + SIZE]
            # face_map = {}
            # for pos in face_map_positions:
            #     face_map[pos] = self.map[pos]

            # print(face_map)
            # exit()


        # 4. map edges -> (from_row, from_col, direction): (to_row, to_col, new_direction)
        self.edge_mapping = {}
        for face in FACES:
            face_rotation = face_definitions[face][2]
            for edge in [0, 1, 2, 3]:
                face_edge = (face_rotation + edge) % 4
                
                other_face = NEXT_FACE[face][rot_edge[edge]][0]
                other_face_rotation = face_definitions[other_face][2]
                other_face_relative_rotation = NEXT_FACE[face][rot_edge[edge]][1]
                # other_edge = (face_edge + face_definitions[other_face][2]) % 4

                # face_edge || other_face_rot || face_definitions[other_face][2]
                # other_edge = ((face_definitions[other_face][2] - face_rotation)) % 4 # closest yet
                other_edge = ((other_face_rotation - face_rotation)) % 4

                for i in range(SIZE):
                    if face_edge == 0:
                        from_row = face_definitions[face][0] * SIZE + 1
                        from_col = face_definitions[face][1] * SIZE + i + 1
                    elif face_edge == 1:
                        from_row = face_definitions[face][0] * SIZE + i + 1
                        from_col = face_definitions[face][1] * SIZE + SIZE
                    elif face_edge == 2:
                        from_row = face_definitions[face][0] * SIZE + SIZE
                        from_col = face_definitions[face][1] * SIZE + SIZE - i
                    elif face_edge == 3:
                        from_row = face_definitions[face][0] * SIZE + SIZE - i
                        from_col = face_definitions[face][1] * SIZE + 1
                    else:
                        assert False

                    # if other_edge == 0:
                    #     to_row = face_definitions[other_face][0] * SIZE + 1
                    #     to_col = face_definitions[other_face][1] * SIZE + i + 1
                    # elif other_edge == 1:
                    #     to_row = face_definitions[other_face][0] * SIZE + i + 1
                    #     to_col = face_definitions[other_face][1] * SIZE + SIZE
                    # elif other_edge == 2:
                    #     to_row = face_definitions[other_face][0] * SIZE + SIZE
                    #     to_col = face_definitions[other_face][1] * SIZE + SIZE - i
                    # elif other_edge == 3:
                    #     to_row = face_definitions[other_face][0] * SIZE + SIZE - i
                    #     to_col = face_definitions[other_face][1] * SIZE + 1
                    # else:
                    #     assert False

                    # most likely correct
                    if other_edge == 0:
                        to_row = face_definitions[other_face][0] * SIZE + SIZE
                        to_col = face_definitions[other_face][1] * SIZE + i + 1
                    elif other_edge == 1:
                        to_row = face_definitions[other_face][0] * SIZE + i + 1
                        to_col = face_definitions[other_face][1] * SIZE + 1
                    elif other_edge == 2:
                        to_row = face_definitions[other_face][0] * SIZE + 1
                        to_col = face_definitions[other_face][1] * SIZE + SIZE - i
                    elif other_edge == 3:
                        to_row = face_definitions[other_face][0] * SIZE + SIZE - i
                        to_col = face_definitions[other_face][1] * SIZE + SIZE
                    else:
                        assert False

                    self.edge_mapping[(from_row, from_col, rot_edge[face_edge])] = (to_row, to_col, rot_edge[other_edge])


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

        part1 = (1000 * position[0]) + (4 * position[1]) + DIRECTION_VALUES[direction]
        
        if self.make_image:
            self.image().save(self.visual_path('map.png'))
            self.image(visited).save(self.visual_path('path-1.png'))
        
        #
        # Part 2
        #
        self.map_edges()

        col = min([coor[1] for coor in self.map if coor[0] == 1])
        position = (1, col)
        direction = 'R'

        visited = set()
        visited.add(position)

        # img = self.image(set(), position)
        # video = cv2.VideoWriter(self.visual_path('part-2.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 5, img.size)
        # video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        for move in self.directions:
            if type(move) == int:
                for _ in range(move):
                    next_dir = direction
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
                        key = (position[0], position[1], direction)
                        assert key in self.edge_mapping

                        next_ = self.edge_mapping[key]
                        next_pos = (next_[0], next_[1])
                        next_dir = next_[2]

                    assert next_pos in self.map

                    if self.map[next_pos] == OPEN:
                        position = next_pos
                        direction = next_dir
                    elif self.map[next_pos] == WALL:
                        break
                    else:
                        assert False

                    visited.add(position)
                    # img = self.image(set(), position)
                    # video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            else:
                direction = NEW_DIRECTION[direction][move]

        # img = self.image(set(), position)
        # for _ in range(5):
        #     video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        # video.release()

        part2 = (1000 * position[0]) + (4 * position[1]) + DIRECTION_VALUES[direction]

        if self.make_image:
            self.image(visited).save(self.visual_path('path-2.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, visited = set(), current: tuple = None):
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

        if current is not None:
            pixels[current[1] - 1, current[0] - 1] = (0, 255, 0)

        scale = 3
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
