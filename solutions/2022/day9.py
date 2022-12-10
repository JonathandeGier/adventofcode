from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

MOVE = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}

# if a leading knot is in one of these relative positions, we do not need to move the current knot
CLOSE_POSITIONS = [
    (-1,  1), (0,  1), (1,  1),
    (-1,  0), (0,  0), (1,  0),
    (-1, -1), (0, -1), (1, -1),
]

# AABCC
# A123C
# H8X4D
# G765E
# GGFEE
# 
# current knot is X, if the previous knot moved to A-H, the current knot must be moved to 1-8
MOVE_TABLE = {
    # A
    (-2, 1): (-1, 1),
    (-2, 2): (-1, 1), # corner
    (-1, 2): (-1, 1),

    # B
    (0, 2): (0, 1),

    # C
    (1, 2): (1, 1),
    (2, 2): (1, 1), # corner
    (2, 1): (1, 1),

    # D
    (2, 0): (1, 0),

    # E
    (1, -2): (1, -1),
    (2, -2): (1, -1), # corner
    (2, -1): (1, -1),

    # F
    (0, -2): (0, -1),

    # G
    (-1, -2): (-1, -1),
    (-2, -2): (-1, -1), # corner
    (-2, -1): (-1, -1),

    # H
    (-2, 0): (-1,  0),
}

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Rope Bridge"
        self.input = self.getInput(self.day)

        self.moves = []

        self.make_image = False
        self.make_video = False
        self.video = None

    def load_moves(self):
        self.moves = []
        for line in self.input.splitlines():
            direction, amount = line.split(' ')
            self.moves.append((direction, int(amount)))

    def move_rope(self, rope: list) -> set:
        tail_visited = set()
        tail_visited.add(rope[-1])

        # min_x, min_y, max_x, max_y
        bounds = (-26, -152, 314, 229)
        if self.make_video:
            img = self.image(bounds, tail_visited, rope)
            self.video = cv2.VideoWriter(self.visual_path('video-rope-' + str(len(rope)) + '.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 30, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        frame = 0
        for move_i, move in enumerate(self.moves):
            for _ in range(move[1]):
                # Move the head
                rope[0] = (rope[0][0] + MOVE[move[0]][0], rope[0][1] + MOVE[move[0]][1])

                # Move the knots
                for i in range(1, len(rope)):
                    knot = rope[i]
                    
                    # determine if the knot needs to be moved
                    move_knot = True
                    for pos_change in CLOSE_POSITIONS:
                        pos = (knot[0] + pos_change[0], knot[1] + pos_change[1])
                        if rope[i-1] == pos:
                            move_knot = False
                            break
                    
                    # if de dont need to move the current knot, we also dont have to move the rest of the knots
                    if not move_knot:
                        break

                    # Move the knot
                    diff = (rope[i-1][0] - knot[0], rope[i-1][1] - knot[1])
                    pos_diff = MOVE_TABLE[diff]
                    rope[i] = (rope[i][0] + pos_diff[0], rope[i][1] + pos_diff[1])

                    # keep track of the visited tail positions
                    if i == len(rope) - 1:
                        tail_visited.add(rope[i])

                # make a video frame
                if self.make_video and frame % 10 == 0:
                    img = self.image(bounds, tail_visited, rope)
                    self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
                    print('move:', move_i)
                frame += 1

        # make end frames and save video
        if self.make_video:
            img = self.image(bounds, tail_visited, rope)
            for _ in range(150):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            cv2.destroyAllWindows()
            self.video.release()

        # make a final image
        if self.make_image:
            self.image(bounds, tail_visited, rope).save(self.visual_path('visited-rope-' + str(len(rope)) + '.png'))

        return tail_visited

    def solve(self):
        start_time = time()

        self.load_moves()

        rope = [(0, 0), (0, 0)]
        tail_visited = self.move_rope(rope)
        part1 = len(tail_visited)

        rope = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        tail_visited = self.move_rope(rope)
        part2 = len(tail_visited)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, bounds: tuple, visited: set, rope: list):
        img = Image.new('RGB', (bounds[2] - bounds[0], bounds[3] - bounds[1]), "black")
        pixels = img.load()
        
        for pos in visited:
            pixels[pos[0] - bounds[0], pos[1] - bounds[1]] = (200, 200, 200)

        for pos in rope:
            pixels[pos[0] - bounds[0], pos[1] - bounds[1]] = (140, 80, 0)

        scale = 4
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img

if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
