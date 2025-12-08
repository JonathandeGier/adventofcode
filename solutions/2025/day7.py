from Table import Table
from time import time
from collections import deque

import cv2
from numpy import asarray

START = 'S'
SPLITTER = '^'
EMPTY = '.'
BEAM = '|'

COLORS = {
    START: (255, 255, 0),
    SPLITTER: (255, 0, 0),
    BEAM: (0, 255, 0),
}

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Laboratories"
        self.input = self.getInput(self.day)

        self.start = None
        self.map = {}

        self.make_visuals = __name__ == '__main__'
        # self.make_visuals = False
        self.video = None
        self.fps = 10

    def solve(self):
        start_time = time()

        # Parse the map
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == START:
                    self.start = (x, y)
                    self.map[x, y] = START
                else:
                    self.map[x, y] = val

        # start a video
        if self.make_visuals:
            img = self.image()
            img.save(self.visual_path('start.png'))

            self.video = cv2.VideoWriter(self.visual_path('part1.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
            for _ in range(self.fps):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # Cascade the beam row by row
        part1 = 0
        next_row = {self.start: 1}
        while next_row:
            row = next_row
            next_row = {}

            for pos in row:
                timelines = row[pos]
                next_pos = (pos[0], pos[1] + 1)

                if next_pos not in self.map:
                    continue

                if self.map[next_pos] == EMPTY or self.map[next_pos] == BEAM:
                    if next_pos in next_row:
                        next_row[next_pos] += timelines
                    else:
                        next_row[next_pos] = timelines

                    self.map[next_pos] = BEAM
                elif self.map[next_pos] == SPLITTER:
                    part1 += 1
                    for dir in [(-1, 0), (1, 0)]:
                        split_next_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])
                        if split_next_pos in next_row:
                            next_row[split_next_pos] += timelines
                        else:
                            next_row[split_next_pos] = timelines
                        self.map[split_next_pos] = BEAM
                else:
                    assert False, 'Unknown map value: ' + self.map[next_pos]

            if self.make_visuals:
                self.video.write(cv2.cvtColor(asarray(self.image()), cv2.COLOR_BGR2RGB))

        part2 = sum([row[pos] for pos in row])

        if self.make_visuals:
            img = self.image()
            img.save(self.visual_path('end.png'))

            for _ in range(self.fps * 10):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            
            self.video.release()
            cv2.destroyAllWindows()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def image(self):
        return self.image_map(self.map, COLORS, scale=5)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
