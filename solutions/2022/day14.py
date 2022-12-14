from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

WALL = '#'
SAND = 'o'
VISITED = '~'

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Regolith Reservoir"
        self.input = self.getInput(self.day)

        self.map = {}
        self.bounds = ()

        self.make_image = False
        self.make_video = False

    def load_map(self):
        self.map = {}
        for line in self.input.splitlines():
            coordinates = [tuple([int(val) for val in coor.split(',')]) for coor in line.split(' -> ')]
            
            for i in range(len(coordinates) - 1):
                _from = coordinates[i]
                _to = coordinates[i+1]

                min_x = min(_from[0], _to[0])
                max_x = max(_from[0], _to[0])
                min_y = min(_from[1], _to[1])
                max_y = max(_from[1], _to[1])

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        self.map[x, y] = WALL

        self.calculate_bounds()

    def calculate_bounds(self):
        min_x = min([coord[0] for coord in self.map.keys()])
        max_x = max([coord[0] for coord in self.map.keys()])
        min_y = min([coord[1] for coord in self.map.keys()])
        max_y = max([coord[1] for coord in self.map.keys()])

        self.bounds = (min_x, max_x, min_y, max_y)

    def drop_sand(self, p2 = False) -> bool:
        current = (500, 0)
        if current in self.map:
            return False

        while True:
            # part 2: floor
            if p2 and current[1] == self.bounds[3] + 1:
                # place the sand
                self.map[current] = SAND
                return True

            # try straight down
            next = (current[0], current[1] + 1)
            if next not in self.map:
                # part 1: check falling into the abyss
                if not p2 and next[1] > self.bounds[3]:
                    return False

                current = next
                continue

            # try falling to the left
            next = (current[0] - 1, current[1] + 1)
            if next not in self.map:
                current = next
                continue

            # try falling to the right
            next = (current[0] + 1, current[1] + 1)
            if next not in self.map:
                current = next
                continue

            # place the sand
            self.map[current] = SAND
            return True


    def solve(self):
        start_time = time()

        self.load_map()

        if self.make_image:
            self.image().save(self.visual_path('map.png'))

        dropped_sand = True
        total_sand = 0
        while dropped_sand:
            dropped_sand = self.drop_sand()
            total_sand += 1

        total_sand -= 1
        part1 = total_sand

        if self.make_image:
            self.image().save(self.visual_path('part1.png'))

        dropped_sand = True
        while dropped_sand:
            dropped_sand = self.drop_sand(True)
            total_sand += 1

        total_sand -= 1
        part2 = total_sand

        if self.make_image:
            self.calculate_bounds()
            self.image().save(self.visual_path('part2.png'))

        if self.make_video:
            self.video('video')

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self):
        img = Image.new('RGB', (self.bounds[1] - self.bounds[0] + 1, self.bounds[3] + 2), "black")
        pixels = img.load()
        for position in self.map:
            if self.map[position] == WALL:
                color = (255, 255, 255)
            elif self.map[position] == SAND:
                color = (245, 204, 71) # sand-ish color
            elif self.map[position] == VISITED:
                color = (125, 103, 34)
            
            img_location = position[0] - self.bounds[0], position[1]
            if 0 < img_location[0] < img.size[0] and 0 < img_location[1] < img.size[1]:
                pixels[img_location] = color

        for x in range(img.size[0]):
            pixels[x, self.bounds[3] + 1] = (255, 255, 255)

        pixels[500 - self.bounds[0], 0] = (125, 103, 34)

        scale = 3
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img

    def video(self, name: str):
        fps = 60
        self.calculate_bounds()
        bounds = self.bounds

        self.load_map()
        self.bounds = bounds

        img = self.image()
        video = cv2.VideoWriter(self.visual_path(name + '.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), fps, img.size)
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # part 1
        while self.drop_sand_visited():
            img = self.image()
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # pause between part 1 and part 2 for 3 seconds
        img = self.image()
        for _ in range(fps * 3):
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # part 2
        frame = 0
        while self.drop_sand_visited(True):
            if frame % 5 == 0:
                img = self.image()
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            frame += 1

        # pause on final image for 5 seconds
        img = self.image()
        for _ in range(fps * 5):
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        video.release()
        cv2.destroyAllWindows()

    # is slower but the visited squares can be visualized
    def drop_sand_visited(self, p2 = False) -> bool:
        current = (500, 0)
        if current in self.map and self.map[current] in [WALL, SAND]:
            return False

        while True:
            self.map[current] = VISITED

            # part 2: floor
            if p2 and current[1] == self.bounds[3] + 1:
                # place the sand
                self.map[current] = SAND
                return True

            # try straight down
            next = (current[0], current[1] + 1)
            if next not in self.map or self.map[next] == VISITED:
                # part 1: check falling into the abyss
                if not p2 and next[1] > self.bounds[3]:
                    return False

                current = next
                continue

            # try falling to the left
            next = (current[0] - 1, current[1] + 1)
            if next not in self.map or self.map[next] == VISITED:
                current = next
                continue

            # try falling to the right
            next = (current[0] + 1, current[1] + 1)
            if next not in self.map or self.map[next] == VISITED:
                current = next
                continue

            # place the sand
            self.map[current] = SAND
            return True



if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
