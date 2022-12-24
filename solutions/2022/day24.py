from Table import Table
from time import time
from collections import deque
from PIL import Image
import cv2
from numpy import asarray

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Blizzard Basin"
        self.input = self.getInput(self.day)

        self.blizzarts = []
        self.width = None
        self.height = None

        self.cached_blizzart_locations = {}

        self.make_images = False
        self.make_video = False

    def load_blizzarts(self):
        self.blizzarts = []
        for y, line in enumerate(self.input.splitlines()[1:-1]):
            for x, val in enumerate(line[1:-1]):
                if val in [UP, DOWN, LEFT, RIGHT]:
                    self.blizzarts.append((x, y, val))
        
        self.width = max([blizzart[0] for blizzart in self.blizzarts]) + 1
        self.height = max([blizzart[1] for blizzart in self.blizzarts]) + 1

    def blizzart_locations(self, minute: int) -> set:
        if minute in self.cached_blizzart_locations:
            return self.cached_blizzart_locations[minute]

        locations = {}
        for blizzart in self.blizzarts:
            if blizzart[2] == UP:
                x = blizzart[0]
                y = (blizzart[1] - minute) % self.height
            elif blizzart[2] == DOWN:
                x = blizzart[0]
                y = (blizzart[1] + minute) % self.height
            elif blizzart[2] == LEFT:
                x = (blizzart[0] - minute) % self.width
                y = blizzart[1]
            elif blizzart[2] == RIGHT:
                x = (blizzart[0] + minute) % self.width
                y = blizzart[1]
            else:
                assert False
            
            if (x, y) not in locations:
                locations[(x, y)] = 1
            else:
                locations[(x, y)] += 1

        self.cached_blizzart_locations[minute] = locations

        return locations

    def move(self, start: tuple, end: tuple, time_spent: int):
        keep_path = self.make_images or self.make_video
        solved = False
        visited = set()
        state = (time_spent, start, [start])
        queue = deque([state])
        while len(queue) > 0:
            time_spent, location, path = queue.popleft()

            if location == end:
                solved = True
                break

            if (time_spent % (self.width * self.height), location) in visited:
                continue

            visited.add((time_spent % (self.width * self.height), location))

            time_spent += 1
            blizzart_locations = self.blizzart_locations(time_spent)

            for dir in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                new_location = (location[0] + dir[0], location[1] + dir[1])
                
                if new_location[0] < 0 or new_location[0] >= self.width or new_location[1] < 0 or new_location[1] >= self.height:
                    if new_location != end:
                        continue

                if (time_spent % (self.width * self.height), new_location) in visited:
                    continue

                if new_location not in blizzart_locations:
                    if keep_path:
                        new_path = path.copy()
                        new_path.append(new_location)
                    else:
                        new_path = []
                    queue.append((time_spent, new_location, new_path))

            if location not in blizzart_locations:
                if keep_path:
                    new_path = path.copy()
                    new_path.append(location)
                else:
                    new_path = []
                queue.append(((time_spent, location, new_path)))
        
        if not solved:
            assert False, 'Not Solved'

        return time_spent, path


    def solve(self):
        start_time = time()

        self.load_blizzarts()

        part1, path1 = self.move((0, -1), (99, 35), 0)
        
        to_start, path2 = self.move((99, 35), (0, -1), part1)
        part2, path3 = self.move((0, -1), (99, 35), to_start)

        if self.make_images:
            self.image().save(self.visual_path('map.png'))
            self.image(path=path1).save(self.visual_path('part1.png'))
            self.image(path=path1 + path2 + path3).save(self.visual_path('part2.png'))

        if self.make_video:
            self.video('video.mp4', path1 + path2 + path3)


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, minute: int = 0, path: list = []):
        img = Image.new('RGB', (self.width + 2, self.height + 2), 'black')
        pixels = img.load()

        locations = self.blizzart_locations(minute)
        for location in locations:
            count = locations[location]
            pixels[location[0] + 1, location[1] + 1] = (50 * count, 50 * count, 50 * count)

        for location in path:
            pixels[location[0] + 1, location[1] + 1] = (255, 255, 0)

        for i in range(self.width + 2):
            if i != 1:
                pixels[i, 0] = (200, 200, 200)
            if i != self.width:
                pixels[i, self.height + 1] = (200, 200, 200)

        for i in range(self.height + 2):
            pixels[0, i] = (200, 200, 200)
            pixels[self.width + 1, i] = (200, 200, 200)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img

    def video(self, name: str, path: list):
        fps = 5
        img = self.image()
        video = cv2.VideoWriter(self.visual_path(name), cv2.VideoWriter_fourcc(*'MP4V'), 5, img.size)
        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        for minute, location in enumerate(path):
            img = self.image(minute, [location])
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        for _ in range(fps * 5):
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
