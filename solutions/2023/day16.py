from Table import Table
from time import time
from collections import deque

from PIL import Image
import cv2
from numpy import asarray

EMPTY = '.'
MIRROR_1 = '/'
MIRROR_2 = '\\'
SPLITTER_1 = '-'
SPLITTER_2 = '|'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

NEW_DIRECTION = {
    EMPTY: {
        UP: [UP],
        DOWN: [DOWN],
        LEFT: [LEFT],
        RIGHT: [RIGHT],
    },
    MIRROR_1: {
        UP: [RIGHT],
        DOWN: [LEFT],
        LEFT: [DOWN],
        RIGHT: [UP],
    },
    MIRROR_2: {
        UP: [LEFT],
        DOWN: [RIGHT],
        LEFT: [UP],
        RIGHT: [DOWN],
    },
    SPLITTER_1: {
        UP: [LEFT, RIGHT],
        DOWN: [LEFT, RIGHT],
        LEFT: [LEFT],
        RIGHT: [RIGHT],
    },
    SPLITTER_2: {
        UP: [UP],
        DOWN: [DOWN],
        LEFT: [UP, DOWN],
        RIGHT: [UP, DOWN],
    },
}

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "The Floor Will Be Lava"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0

        self.make_video = False and __name__ == '__main__'
        self.fps = 30
        self.video = None

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = val
        self.max_x = x
        self.max_y = y

    def move(self, pos: tuple, dir: str) -> tuple:
        if dir == UP:
            return (pos[0], pos[1] - 1)
        elif dir == DOWN:
            return (pos[0], pos[1] + 1)
        elif dir == LEFT:
            return (pos[0] - 1, pos[1])
        elif dir == RIGHT:
            return (pos[0] + 1, pos[1])
        else:
            assert False, f'Unknown direction {dir}'

    def energize(self, start_pos: tuple, start_dir: str, add_frames: bool = False) -> int:
        explored = set()
        energized = set()
        prev_dist = 0
        queue = deque([(start_pos, start_dir, prev_dist)])
        while queue:
            pos, dir, dist = queue.popleft()
            if (pos, dir) in explored:
                continue

            energized.add(pos)
            explored.add((pos, dir))

            if add_frames and prev_dist != dist:
                img = self.image(explored)
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
                prev_dist = dist

            new_dirs = NEW_DIRECTION[self.map[pos]][dir]
            for new_dir in new_dirs:
                new_pos = self.move(pos, new_dir)

                if new_pos not in self.map:
                    continue

                queue.append((new_pos, new_dir, dist + 1))
        
        return (len(energized), explored)


    def solve(self):
        start_time = time()

        self.parse_map()
        img = self.image()
        img.save(self.visual_path('mirrors.png'))

        if self.make_video:
            self.video = cv2.VideoWriter(self.visual_path('part1.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
            for _ in range(self.fps):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        part1, explored = self.energize((0, 0), RIGHT, self.make_video)
        img = self.image(explored)
        img.save(self.visual_path('part1.png'))

        if self.make_video:
            for _ in range(self.fps * 5):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            self.video.release()
            cv2.destroyAllWindows()

        part2 = 0
        max_pos = max_dir = None
        for x in range(self.max_x + 1):
            for y, dir in ((0, DOWN), (self.max_y, UP)):
                energized = max(part2, self.energize((x, y), dir)[0])
                if energized > part2:
                    part2 = energized
                    max_pos = (x, y)
                    max_dir = dir
            
        for y in range(self.max_y + 1):
            for x, dir in ((0, RIGHT), (self.max_x, LEFT)):
                energized = max(part2, self.energize((x, y), dir)[0])
                if energized > part2:
                    part2 = energized
                    max_pos = (x, y)
                    max_dir = dir

        # Make video of part 2
        if self.make_video:
            img = self.image()
            self.video = cv2.VideoWriter(self.visual_path('part2.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
            for _ in range(self.fps):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        explored = self.energize(max_pos, max_dir, self.make_video)[1]
        img = self.image(explored)
        img.save(self.visual_path('part2.png'))

        if self.make_video:
            for _ in range(self.fps * 5):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            self.video.release()
            cv2.destroyAllWindows()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


    def image(self, explored: set() = {}):
        mirror_color = (0, 200, 200)
        light_color = (200, 200, 200)

        img = Image.new('RGB', ((self.max_x + 1) * 3, (self.max_y + 1) * 3), "black")
        pixels = img.load()
        for pos in self.map:
            pixel_pos = (pos[0] * 3, pos[1] * 3)
            if self.map[pos] == MIRROR_1: # /
                pixels[pixel_pos[0] + 2, pixel_pos[1] + 0] = mirror_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = mirror_color
                pixels[pixel_pos[0] + 0, pixel_pos[1] + 2] = mirror_color

                if (pos, RIGHT) in explored or (pos, DOWN) in explored:
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 0] = light_color
                    pixels[pixel_pos[0] + 0, pixel_pos[1] + 1] = light_color
                if (pos, LEFT) in explored or (pos, UP) in explored:
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 2] = light_color
                    pixels[pixel_pos[0] + 2, pixel_pos[1] + 1] = light_color
            elif self.map[pos] == MIRROR_2: # \
                pixels[pixel_pos[0] + 0, pixel_pos[1] + 0] = mirror_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = mirror_color
                pixels[pixel_pos[0] + 2, pixel_pos[1] + 2] = mirror_color

                if (pos, RIGHT) in explored or (pos, UP) in explored:
                    pixels[pixel_pos[0] + 0, pixel_pos[1] + 1] = light_color
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 2] = light_color
                if (pos, LEFT) in explored or (pos, DOWN) in explored:
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 0] = light_color
                    pixels[pixel_pos[0] + 2, pixel_pos[1] + 1] = light_color
            elif self.map[pos] == SPLITTER_1: # -
                pixels[pixel_pos[0] + 0, pixel_pos[1] + 1] = mirror_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = mirror_color
                pixels[pixel_pos[0] + 2, pixel_pos[1] + 1] = mirror_color

                if (pos, UP) in explored:
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 2] = light_color
                if (pos, DOWN) in explored:
                    pixels[pixel_pos[0] + 1, pixel_pos[1] + 0] = light_color
            elif self.map[pos] == SPLITTER_2: # |
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 0] = mirror_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = mirror_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 2] = mirror_color

                if (pos, LEFT) in explored:
                    pixels[pixel_pos[0] + 2, pixel_pos[1] + 1] = light_color
                if (pos, RIGHT) in explored:
                    pixels[pixel_pos[0] + 0, pixel_pos[1] + 1] = light_color

        for pos, dir in explored:
            if self.map[pos] != EMPTY:
                continue

            pixel_pos = (pos[0] * 3, pos[1] * 3)

            if dir in (UP, DOWN):
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 0] = light_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = light_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 2] = light_color
            if dir in (LEFT, RIGHT):
                pixels[pixel_pos[0] + 0, pixel_pos[1] + 1] = light_color
                pixels[pixel_pos[0] + 1, pixel_pos[1] + 1] = light_color
                pixels[pixel_pos[0] + 2, pixel_pos[1] + 1] = light_color

        img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.Resampling.NEAREST)
        return img


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
