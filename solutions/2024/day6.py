from Table import Table
from time import time

import cv2
from numpy import asarray

OBSTACLE = '#'
EMPTY = '.'

NEXT_DIR = {
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
    (1, 0): (0, 1),
}

COLORS = {
    '#': (0, 200, 0), 
    'X': (150, 150, 150),
    'G': (255, 255, 255),
}

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Guard Gallivant"
        self.input = self.getInput(self.day)

        self.map = {}
        self.obstacles = set()
        self.guard_start = None
        self.guard = None
        self.guard_dir = None

        self.make_visuals = __name__ == '__main__'
        self.fps = 60
        self.video = None


    def parse_map(self):
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == '^':
                    self.guard = (x, y)
                    self.guard_start = (x, y)
                    self.guard_dir = (0, -1)
                    self.map[x, y] = '.'
                else:
                    self.map[x, y] = val
                    if val == OBSTACLE:
                        self.obstacles.add((x, y))


    def solve(self):
        start_time = time()

        loop_positions = set()
        self.parse_map()
        visited = {}
        self.setup_video()
        frame_counter = 0
        while True:
            if self.guard not in visited:
                visited[self.guard] = []

            if frame_counter % 3 == 0:
                self.add_frame(visited)
            frame_counter += 1

            look_dir = NEXT_DIR[self.guard_dir]
            look_pos = self.guard
            look_visited = {}
            potential_obstacle = (self.guard[0] + self.guard_dir[0], self.guard[1] + self.guard_dir[1])
            does_loop = False
            while True:
                if potential_obstacle not in self.map or potential_obstacle in visited:
                    break

                if look_pos in visited and look_dir in visited[look_pos]:
                    # Case 1: the guard already visited this position in this direction, loop detected
                    does_loop = True
                    break

                if look_pos not in look_visited:
                    look_visited[look_pos] = []
                elif look_dir in look_visited[look_pos]:
                    # Case 2
                    does_loop = True
                    break


                look_visited[look_pos].append(look_dir)

                look_next_pos = (look_pos[0] + look_dir[0], look_pos[1] + look_dir[1])
                if look_next_pos not in self.map:
                    break

                if self.map[look_next_pos] == OBSTACLE or look_next_pos == potential_obstacle:
                    look_dir = NEXT_DIR[look_dir]
                else:
                    look_pos = look_next_pos

            if does_loop:
                loop_positions.add(potential_obstacle)

            visited[self.guard].append(self.guard_dir)

            next_pos = (self.guard[0] + self.guard_dir[0], self.guard[1] + self.guard_dir[1])
            if next_pos not in self.map:
                break

            if self.map[next_pos] == OBSTACLE:
                self.guard_dir = NEXT_DIR[self.guard_dir]
            else:
                self.guard = next_pos

        if self.make_visuals:
            self.finish_video(visited)

            self.image_map(self.map, {'#': (0, 200, 0)}, scale=5).save(self.visual_path('map.png'))

            path_data = self.map.copy()
            for pos in visited:
                path_data[pos] = 'X'

            self.image_map(path_data, {'#': (0, 200, 0), 'X': (100, 100, 100)}, scale=5).save(self.visual_path('path.png'))

        part1 = len(visited.keys())
        part2 = len(loop_positions)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


    def setup_video(self):
        if not self.make_visuals:
            return

        data = self.map.copy()
        data[self.guard] = 'G'
        img = self.image_map(data, COLORS, scale=5)

        self.video = cv2.VideoWriter(self.visual_path('part1.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
        for _ in range(self.fps):
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

    def add_frame(self, visited: dict):
        if not self.make_visuals:
            return

        data = self.map.copy()
        for pos in visited:
            data[pos] = 'X'
        data[self.guard] = 'G'

        img = self.image_map(data, COLORS, scale=5)
        self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

    def finish_video(self, visited: dict):
        if not self.make_visuals:
            return
        
        data = self.map.copy()
        for pos in visited:
            data[pos] = 'X'
        data[self.guard] = 'G'

        img = self.image_map(data, COLORS, scale=5)
        for _ in range(self.fps * 5):
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        
        self.video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")


