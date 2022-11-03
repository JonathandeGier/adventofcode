from collections import Counter
from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

OPEN = '.'
TREES = '|'
LUMBER = '#'

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "Settlers of The North Pole"
        self.input = self.getInput(self.day)

        self.make_video = True
        self.video = None

        self.map = None

    def load_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = val

    def step(self):
        new_map = {}
        for item in self.map.items():
            pos = item[0]
            val = item[1]

            adjacent = []
            for diff in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                adjacent_position = (pos[0] + diff[0], pos[1] + diff[1])
                if adjacent_position in self.map:
                    adjacent.append(self.map[adjacent_position])

            count = Counter(adjacent)
            
            if val == OPEN:
                if count[TREES] >= 3:
                    new_map[pos] = TREES
                else:
                    new_map[pos] = OPEN
            elif val == TREES:
                if count[LUMBER] >= 3:
                    new_map[pos] = LUMBER
                else:
                    new_map[pos] = TREES
            elif val == LUMBER:
                if count[LUMBER] >= 1 and count[TREES] >= 1:
                    new_map[pos] = LUMBER
                else:
                    new_map[pos] = OPEN
        
        self.map = new_map

    def solve(self):
        start_time = time()

        self.load_map()
        for _ in range(10):
            self.step()

        trees = len([val for val in self.map.values() if val == TREES])
        lumber = len([val for val in self.map.values() if val == LUMBER])

        part1 = trees * lumber

        self.load_map()

        if self.make_video:
            img = self.image()
            self.video = cv2.VideoWriter('solutions/2018/visuals/day18/video.avi', 0, 30, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        seen = {}
        for i in range(1_000_000_000):
            map_hash = hash(frozenset(self.map.items()))
            if map_hash in seen:
                break
            
            seen[map_hash] = i
            
            self.step()

            if self.make_video:
                img = self.image()
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        left = (1_000_000_000 - i) % (i - seen[map_hash])
        for _ in range(left):
            self.step()

            if self.make_video:
                img = self.image()
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        if self.make_video:
            cv2.destroyAllWindows()
            self.video.release()

        trees = len([val for val in self.map.values() if val == TREES])
        lumber = len([val for val in self.map.values() if val == LUMBER])

        # 207570 < x < ...
        part2 = trees * lumber

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self):
        img = Image.new('RGB', (50, 50), "black")
        pixels = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if self.map[x, y] == '.':
                    pixels[x,y] = (0, 255, 0)
                elif self.map[x, y] == '|':
                    pixels[x,y] = (0, 110, 0)
                elif self.map[x, y] == '#':
                    pixels[x,y] = (207, 160, 41)
                else:
                    pixels[x,y] = (255, 255, 255)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.NEAREST)

        return img


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
