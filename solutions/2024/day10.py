from Table import Table
from time import time
from collections import deque

import cv2
from numpy import asarray

COLORS = {
    0: (10, 10, 10),
    1: (20, 20, 20),
    2: (30, 30, 30),
    3: (40, 40, 40),
    4: (50, 50, 50),
    5: (60, 60, 60),
    6: (70, 70, 70),
    7: (80, 80, 80),
    8: (90, 90, 90),
    9: (100, 100, 100),
}

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Hoof It"
        self.input = self.getInput(self.day)

        self.map = {}
        self.heads = []

    def parse_map(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[x, y] = int(val)
                if val == '0':
                    self.heads.append((x, y))

    def solve(self):
        start_time = time()

        self.parse_map()

        part1 = 0
        part2 = 0
        trails = []
        for head in self.heads:
            reachable_tops = set()
            paths = 0
            visited = set()
            queue = deque([head])
            while len(queue) > 0:
                pos = queue.popleft()

                visited.add(pos)

                if self.map[pos] == 9:
                    paths += 1
                    reachable_tops.add(pos)
                    continue

                for dir in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    next_pos = (pos[0] + dir[0], pos[1] + dir[1])

                    if next_pos not in self.map:
                        continue

                    if self.map[next_pos] != self.map[pos] + 1:
                        continue

                    queue.append(next_pos)

            trails.append(visited)
            part1 += len(reachable_tops)
            part2 += paths

        self.visuals(trails)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def visuals(self, trails):
        if __name__ != '__main__':
            return

        # image of the hightmap, grayscale
        img = self.image_map(self.map, COLORS, scale=10)
        img.save(self.visual_path('map.png'))
        
        # defining trail colors
        for i, col in enumerate([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1)]):
            for val in range(10):
                COLORS[str(i) + str(val)] = ((COLORS[val][0] + 100) * col[0], (COLORS[val][1] + 100) * col[1], (COLORS[val][2] + 100) * col[2])
        
        video = cv2.VideoWriter(self.visual_path('trails.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 10, img.size)
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # editing map to add trails
        for i, trail in enumerate(trails):
            col = i % 6
            for pos in trail:
                if type(self.map[pos]) != int:
                    continue
                self.map[pos] = str(col) + str(self.map[pos])

            img = self.image_map(self.map, COLORS, scale=10)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # colored trails, brighter is higher
        img = self.image_map(self.map, COLORS, scale=10)
        img.save(self.visual_path('trails.png'))

        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
