from Table import Table
from time import time
from collections import deque
import math

from PIL import Image
import cv2
from numpy import asarray

PIPE_NORTH_SOUTH = '|'
PIPE_EAST_WEST = '-'
PIPE_NORTH_EAST = 'L'
PIPE_NORTH_WEST = 'J'
PIPE_SOUTH_WEST = '7'
PIPE_SOUTH_EAST = 'F'

NORTH = ( 0, -1)
SOUTH = ( 0,  1)
EAST =  ( 1,  0)
WEST =  (-1,  0)

NORTH_EAST = ( 1, -1)
NORTH_WEST = (-1, -1)
SOUTH_EAST = ( 1,  1)
SOUTH_WEST = (-1,  1)

DIRECTIONS = {
    PIPE_NORTH_SOUTH: [NORTH, SOUTH],
    PIPE_EAST_WEST:   [EAST, WEST],
    PIPE_NORTH_EAST:  [NORTH, EAST],
    PIPE_NORTH_WEST:  [NORTH, WEST],
    PIPE_SOUTH_WEST:  [SOUTH, WEST],
    PIPE_SOUTH_EAST:  [SOUTH, EAST],
}

# . . . . . . . . . . . . . . .
# . O O O O O O O O O O O O O .
# . O F--------->---------7 O .
# . O | I I I I I I I I I | O .
# . O | I F-----<-----7 I | O .
# . O ^ I | O O O O O | I v O .
# . O | I | O O O O O | I | O .
# . O | I L---7 O F---J I | O .
# . O | I I I | O | I I I | O .
# . O L-------J O L-------J O .
# . O O O O O O O O O O O O O .
# . . . . . . . . . . . . . . . 
EDGES = {
    PIPE_NORTH_SOUTH: { # | current pipe
        SOUTH: ((EAST,), (WEST,)), # current direction: inside points, outside points
        NORTH: ((WEST,), (EAST,)),
    },
    PIPE_EAST_WEST: { # -
        WEST: ((SOUTH,), (NORTH,)),
        EAST: ((NORTH,), (SOUTH,)),
    },
    PIPE_NORTH_EAST: { # L
        EAST: ((), (SOUTH, SOUTH_WEST, WEST)),
        NORTH: ((SOUTH, SOUTH_WEST, WEST), ()),
    },
    PIPE_NORTH_WEST: { # J
        NORTH: ((), (EAST, SOUTH_EAST, SOUTH)),
        WEST: ((EAST, SOUTH_EAST, SOUTH), ()),
    },
    PIPE_SOUTH_WEST: { # 7
        WEST: ((), (NORTH, NORTH_EAST, EAST)),
        SOUTH: ((NORTH, NORTH_EAST, EAST), ()),
    },
    PIPE_SOUTH_EAST: { # F
        SOUTH: ((), (WEST, NORTH_WEST, NORTH)),
        EAST: ((WEST, NORTH_WEST, NORTH), ()),
    },
}

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Pipe Maze"
        self.input = self.getInput(self.day)

        self.map = {}

        self.make_image = False and __name__ == "__main__"
        self.make_video = False and __name__ == "__main__"
        self.fps = 60
        self.video = None
        self.latest_frame = None

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = val

    def expand_bfs(self, points: set, main_loop: set(), add_frames: bool = False, other_points: set = set()) -> set:
        expanded_points = set()
        
        queue = deque()
        for point in points:
            if point not in main_loop:
                queue.append(point)

        while queue:
            point = queue.popleft()
            if point in expanded_points:
                continue

            expanded_points.add(point)
            if add_frames and point not in points:
                self.add_frame(main_loop, expanded_points, other_points)

            for dir in (NORTH, EAST, SOUTH, WEST):
                new_point = (point[0] + dir[0], point[1] + dir[1])

                if (new_point not in expanded_points) and (new_point in self.map) and (new_point not in main_loop):
                    queue.append(new_point)

        return expanded_points

    def solve(self):
        start_time = time()

        self.parse_map()

        # Get the start position
        pos = [key for key in self.map if self.map[key] == 'S'][0]

        # Determine the pipe under the start position
        connects_north = self.map[(pos[0] + NORTH[0], pos[1] + NORTH[1])] in (PIPE_NORTH_SOUTH, PIPE_SOUTH_EAST, PIPE_SOUTH_WEST)
        connects_east  = self.map[(pos[0] + EAST[0] , pos[1] + EAST[1] )] in (PIPE_EAST_WEST, PIPE_NORTH_WEST, PIPE_SOUTH_WEST)
        connects_south = self.map[(pos[0] + SOUTH[0], pos[1] + SOUTH[1])] in (PIPE_NORTH_SOUTH, PIPE_NORTH_EAST, PIPE_NORTH_WEST)
        connects_west  = self.map[(pos[0] + WEST[0] , pos[1] + WEST[1] )] in (PIPE_EAST_WEST, PIPE_NORTH_EAST, PIPE_SOUTH_EAST)
        
        if sum([connects_north, connects_east, connects_south, connects_west]) != 2:
            assert False, 'Cannot determine pipe under starting position'

        if connects_north and connects_south:
            pipe = PIPE_NORTH_SOUTH
        elif connects_north and connects_east:
            pipe = PIPE_NORTH_EAST
        elif connects_north and connects_west:
            pipe = PIPE_NORTH_WEST
        elif connects_south and connects_east:
            pipe = PIPE_SOUTH_EAST
        elif connects_south and connects_west:
            pipe = PIPE_SOUTH_WEST
        elif connects_east and connects_west:
            pipe = PIPE_EAST_WEST
        else:
            assert False

        self.map[pos] = pipe

        self.start_video('video.mp4')

        # Go through the pipe
        main_loop = set()
        inside = set()
        outside = set()
        frame = 0
        while True:
            main_loop.add(pos)

            # Determine new direction
            new_pos = None
            for dir in DIRECTIONS[self.map[pos]]:
                dir_pos = (pos[0] + dir[0], pos[1] + dir[1])
                if dir_pos not in main_loop:
                    new_pos = dir_pos
                    break

            # If we can't go further, it means we are at the end of the loop
            if new_pos is None:
                break

            # Label the inside and outside edges
            for edge in EDGES[self.map[pos]][dir][0]:
                inside.add((pos[0] + edge[0], pos[1] + edge[1]))
            for edge in EDGES[self.map[pos]][dir][1]:
                outside.add((pos[0] + edge[0], pos[1] + edge[1]))

            pos = new_pos

            # only for video: start slow and speed up
            if frame < self.fps * 5:
                self.add_frame(main_loop, inside, outside)
                self.add_frame(main_loop, inside, outside)
            elif frame < self.fps * 10:
                self.add_frame(main_loop, inside, outside)
            elif frame % 5 == 0:
                self.add_frame(main_loop, inside, outside)
            
            frame += 1

        part1 = len(main_loop) // 2

        self.add_frame(main_loop, inside, outside)
        self.pause(1)

        all_inside = self.expand_bfs(inside, main_loop, True, outside)
        all_outside = self.expand_bfs(outside, main_loop)

        # "inside" can also be the outside, so i pick the smalles of the two
        part2 = min(len(all_inside), len(all_outside))

        self.pause(5)
        self.end_video()

        end_time = time()
        seconds_elapsed = end_time - start_time

        if self.make_image:
            self.image(main_loop, set(), set()).save(self.visual_path('pipe.png'))
            self.image(main_loop, inside, outside).save(self.visual_path('pipe_edges.png'))
            self.image(main_loop, all_inside, all_outside).save(self.visual_path('pipe_edges_filled.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)
    

    def image(self, main_loop: set, inside: set, outside: set):
        max_x = max([pos[0] for pos in self.map.keys()])
        max_y = max([pos[1] for pos in self.map.keys()])

        img = Image.new('RGB', (max_x + 1, max_y + 1), "black")
        pixels = img.load()
        for pos in inside:
            pixels[pos] = (200, 200, 0)
        for pos in outside:
            pixels[pos] = (200, 0, 0)
        for pos in main_loop:
            pixels[pos] = (0, 200, 200)

        scale = 8
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img
    
    def start_video(self, name):
        if not self.make_video:
            return

        img = self.image(set(), set(), set())

        self.video = cv2.VideoWriter(self.visual_path(name), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
        self.latest_frame = img
        self.pause(1)

    def add_frame(self, main_loop: set, inside: set, outside: set):
        if not self.make_video:
            return
        
        self.latest_frame = self.image(main_loop, inside, outside)
        self.video.write(cv2.cvtColor(asarray(self.latest_frame), cv2.COLOR_BGR2RGB))

    def pause(self, seconds: float):
        if not self.make_video:
            return
        
        for _ in range(math.floor(self.fps * seconds)):
            self.video.write(cv2.cvtColor(asarray(self.latest_frame), cv2.COLOR_BGR2RGB))

    def end_video(self):
        if not self.make_video:
            return

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
