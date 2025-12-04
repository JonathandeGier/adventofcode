from Table import Table
from time import time

import cv2
from numpy import asarray

PAPER = '@'

COLORS = {
    PAPER: (255, 255, 255)
}

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Printing Department"
        self.input = self.getInput(self.day)

        self.make_visuals = __name__ == '__main__'
        # self.make_visuals = False
        self.fps = 2
        self.video = None

        self.map = {}

    def solve(self):
        start_time = time()

        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == PAPER:
                    self.map[x, y] = PAPER

        if self.make_visuals:
            img = self.image()
            img.save(self.visual_path('start.png'))
            self.video = cv2.VideoWriter(self.visual_path('part2.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
            for _ in range(self.fps):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        i = 0
        part1 = 0
        part2 = 0
        while True:
            # Select all paper rolls to remove
            to_remove = []
            for pos in self.map:
                neighbours = 0
                for dir in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    other_pos = (pos[0] + dir[0], pos[1] + dir[1])
                    if other_pos in self.map:
                        neighbours += 1

                if neighbours < 4:
                    to_remove.append(pos)

                    part2 += 1
                    if i == 0:
                        part1 += 1

            # if there is nothing to remove, we are done
            if len(to_remove) == 0:
                break

            # remove the selected rolls
            for pos in to_remove:
                del self.map[pos]

            i += 1

            if self.make_visuals:
                self.video.write(cv2.cvtColor(asarray(self.image()), cv2.COLOR_BGR2RGB))
            
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
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
