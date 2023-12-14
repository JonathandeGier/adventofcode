from Table import Table
from time import time

import cv2
from numpy import asarray

BLOCK = '#'
STONE = 'O'
EMPTY = '.'

COLORS = {
    STONE: (200, 200, 200), 
    BLOCK: (90, 90, 90),
    EMPTY: (0, 0, 0),
}

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Parabolic Reflector Dish"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0

        self.make_video = True and __name__ == '__main__'
        self.video = None

    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == '.':
                    continue
                self.map[(x, y)] = val
        
        self.max_x = max([pos[0] for pos in self.map.keys()])
        self.max_y = max([pos[1] for pos in self.map.keys()])


    def move_north(self, add_frames: bool = False):
        stones = sorted([pos for pos in self.map if self.map[pos] == STONE], key=lambda pos: (pos[1], pos[0]))
        prev_y = 0
        for stone in stones:
            if prev_y != stone[1] and add_frames:
                self.add_frame()
                prev_y = stone[1]

            if stone[1] == 0:
                continue

            new_y = stone[1]
            for y in range(stone[1] - 1, -1, -1):
                if (stone[0], y) not in self.map:
                    new_y = y
                else:
                    break

            del self.map[stone]
            self.map[(stone[0], new_y)] = STONE                


    def move_south(self, add_frames: bool = False):
        stones = sorted([pos for pos in self.map if self.map[pos] == STONE], key=lambda pos: (pos[1], pos[0]), reverse=True)
        prev_y = self.max_y
        for stone in stones:
            if prev_y != stone[1] and add_frames:
                self.add_frame()
                prev_y = stone[1]

            if stone[1] == self.max_y:
                continue

            new_y = stone[1]
            for y in range(stone[1] + 1, self.max_y + 1):
                if (stone[0], y) not in self.map:
                    new_y = y
                else:
                    break

            del self.map[stone]
            self.map[(stone[0], new_y)] = STONE


    def move_west(self, add_frames: bool = False):
        stones = sorted([pos for pos in self.map if self.map[pos] == STONE], key=lambda pos: pos)
        prev_x = 0
        for stone in stones:
            if prev_x != stone[0] and add_frames:
                self.add_frame()
                prev_x = stone[0]

            if stone[0] == 0:
                continue

            new_x = stone[0]
            for x in range(stone[0] - 1, -1, -1):
                if (x, stone[1]) not in self.map:
                    new_x = x
                else:
                    break

            del self.map[stone]
            self.map[(new_x, stone[1])] = STONE


    def move_east(self, add_frames: bool = False):
        stones = sorted([pos for pos in self.map if self.map[pos] == STONE], key=lambda pos: pos, reverse=True)
        prev_x = self.max_x
        for stone in stones:
            if prev_x != stone[0] and add_frames:
                self.add_frame()
                prev_x = stone[0]

            if stone[0] == self.max_x:
                continue

            new_x = stone[0]
            for x in range(stone[0] + 1, self.max_x + 1):
                if (x, stone[1]) not in self.map:
                    new_x = x
                else:
                    break

            del self.map[stone]
            self.map[(new_x, stone[1])] = STONE


    def round(self, add_frames: bool = False):
        self.move_north(add_frames)
        self.move_west(add_frames)
        self.move_south(add_frames)
        self.move_east(add_frames)


    def cycle(self, rounds: int):
        seen = {}
        for i in range(1, rounds):
            self.round()

            key = frozenset([pos for pos in self.map if self.map[pos] == STONE])
            if key not in seen:
                seen[key] = i
            else:
                diff = i - seen[key]
                remain = (rounds - i) % diff

                for _ in range(remain):
                    self.round()

                break


    def solve(self):
        start_time = time()

        self.parse_map()
        self.image().save(self.visual_path('start.png'))

        self.move_north()
        part1 = sum([self.max_y - pos[1] + 1 for pos in self.map if self.map[pos] == STONE])
        self.image().save(self.visual_path('part1.png'))

        self.parse_map()
        self.cycle(1_000_000_000)
        part2 = sum([self.max_y - pos[1] + 1 for pos in self.map if self.map[pos] == STONE])

        end_time = time()
        seconds_elapsed = end_time - start_time

        self.image().save(self.visual_path('billion.png'))
        if self.make_video:
            self.render_video('cycles.mp4')

        return (self.day, self.title, part1, part2, seconds_elapsed)


    def render_video(self, name: str):
        fps = 60

        self.parse_map()
        img = self.image()
        self.video = cv2.VideoWriter(self.visual_path(name), cv2.VideoWriter_fourcc(*'mp4v'), fps, img.size)
        
        for _ in range(fps * 2):
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        for _ in range(10):
            self.round(True)

        img = self.image()
        for _ in range(fps * 5):
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        self.video.release()
        cv2.destroyAllWindows()


    def add_frame(self):
        self.video.write(cv2.cvtColor(asarray(self.image()), cv2.COLOR_BGR2RGB))

    def image(self):
        return self.image_map(self.map, COLORS, scale=5)


    def print_map(self, title: str = ''):
        max_x = max([pos[0] for pos in self.map.keys()])
        max_y = max([pos[1] for pos in self.map.keys()])

        if title != '':
            print(title)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if (x, y) in self.map:
                    print(self.map[(x, y)], end='')
                else:
                    print('.', end='')
            print('')
        print('')


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
