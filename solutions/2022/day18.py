from Table import Table
from time import time
from collections import deque
from PIL import Image
import cv2
from numpy import asarray

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "Boiling Boulders"
        self.input = self.getInput(self.day)
        
        self.make_video = True

        self.droplets = set()

        self.min_x = None
        self.min_y = None
        self.min_z = None

        self.max_x = None
        self.max_y = None
        self.max_z = None


    def load_droplets(self):
        self.droplets = set()
        for line in self.input.splitlines():
            self.droplets.add(tuple([int(val) for val in line.split(',')]))

        self.min_x = min([drop[0] for drop in self.droplets]) - 1
        self.min_y = min([drop[1] for drop in self.droplets]) - 1
        self.min_z = min([drop[2] for drop in self.droplets]) - 1

        self.max_x = max([drop[0] for drop in self.droplets]) + 1
        self.max_y = max([drop[1] for drop in self.droplets]) + 1
        self.max_z = max([drop[2] for drop in self.droplets]) + 1


    def solve(self):
        start_time = time()

        self.load_droplets()

        surface = 0
        for droplet in self.droplets:
            for side in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
                new_droplet = (droplet[0] + side[0], droplet[1] + side[1], droplet[2] + side[2])

                if new_droplet not in self.droplets:
                    surface += 1

        part1 = surface

        # Use BFS to go around the droplets and count the edges
        visited = set()
        external_surface = 0
        queue = deque()
        queue.append((self.min_x, self.min_y, self.min_z))
        while len(queue) > 0:
            pos = queue.popleft()
            assert pos not in self.droplets

            if pos in visited:
                continue

            visited.add(pos)

            for side in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
                new_pos = (pos[0] + side[0], pos[1] + side[1], pos[2] + side[2])

                if new_pos[0] < self.min_x or new_pos[0] > self.max_x or new_pos[1] < self.min_y or new_pos[1] > self.max_y or new_pos[2] < self.min_z or new_pos[2] > self.max_z:
                    continue

                if new_pos in self.droplets:
                    external_surface += 1
                else:
                    if new_pos in visited:
                        continue

                    queue.append(new_pos)

        part2 = external_surface

        if self.make_video:
            img = self.image(self.min_z)
            video = cv2.VideoWriter(self.visual_path('slices.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 5, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            for z in range(self.min_y, self.max_z + 1):
                img = self.image(z)
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            video.release()
            cv2.destroyAllWindows()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, z: int):
        img = Image.new('RGB', (self.max_x - self.min_x + 1, self.max_y - self.min_y + 1), 'black')
        pixels = img.load()
        for pos in [pos for pos in self.droplets if pos[2] == z]:
            pixels[pos[0] - self.min_x, pos[1] - self.min_y] = (255, 255, 255)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img



if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
