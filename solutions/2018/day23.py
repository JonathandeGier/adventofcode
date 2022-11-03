import heapq
from Table import Table
from time import time
from PIL import Image

class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __str__(self) -> str:
        return str((self.x, self.y, self.z))

class Box:
    def __init__(self, min: Point, size: Point):
        # all inclusive
        self.min = min
        self.max = Point(min.x + size.x - 1, min.y + size.y - 1, min.z + size.z - 1)
        self.size = size

    def corners(self):
        return [
            Point(self.min.x, self.min.y, self.min.z),
            Point(self.max.x, self.min.y, self.min.z),
            Point(self.min.x, self.max.y, self.min.z),
            Point(self.max.x, self.max.y, self.min.z),
            
            Point(self.min.x, self.min.y, self.max.z),
            Point(self.max.x, self.min.y, self.max.z),
            Point(self.min.x, self.max.y, self.max.z),
            Point(self.max.x, self.max.y, self.max.z),
        ]

    def distance(self, position: Point):
        return min([abs(corner.x - position.x) + abs(corner.y - position.y) + abs(corner.z - position.z) for corner in self.corners()])

    def divide(self):
        size_x  = self.size.x // 2
        other_x = self.size.x - size_x
        size_y  = self.size.y // 2
        other_y = self.size.y - size_y
        size_z  = self.size.z // 2
        other_z = self.size.z - size_z

        boxes = [
            Box(Point(self.min.x,          self.min.y,          self.min.z),          Point(size_x,  size_y,  size_z)),
            Box(Point(self.min.x + size_x, self.min.y,          self.min.z),          Point(other_x, size_y,  size_z)),
            Box(Point(self.min.x,          self.min.y + size_y, self.min.z),          Point(size_x,  other_y, size_z)),
            Box(Point(self.min.x + size_x, self.min.y + size_y, self.min.z),          Point(other_x, other_y, size_z)),

            Box(Point(self.min.x,          self.min.y,          self.min.z + size_z), Point(size_x,  size_y,  other_z)),
            Box(Point(self.min.x + size_x, self.min.y,          self.min.z + size_z), Point(other_x, size_y,  other_z)),
            Box(Point(self.min.x,          self.min.y + size_y, self.min.z + size_z), Point(size_x,  other_y, other_z)),
            Box(Point(self.min.x + size_x, self.min.y + size_y, self.min.z + size_z), Point(other_x, other_y, other_z)),
        ]

        return [box for box in boxes if box.size.x > 0 and box.size.y > 0 and box.size.z > 0]

    def computed_size(self):
        return self.size.x * self.size.y * self.size.z

    def __gt__(self, other) -> bool:
        return True

    def __str__(self) -> str:
        return str(self.min) + " -> " + str(self.max)

class NanoBot:
    def __init__(self, id: int, position: Point, radius: int):
        self.id = id
        self.position = position
        self.radius = radius

    def in_range(self, point: Point):
        return self.position.distance(point) <= self.radius

    def intersects(self, box: Box):
        dx = max(0, max(box.min.x - self.position.x, self.position.x - box.max.x))
        dy = max(0, max(box.min.y - self.position.y, self.position.y - box.max.y))
        dz = max(0, max(box.min.z - self.position.z, self.position.z - box.max.z))

        return abs(dx) + abs(dy) + abs(dz) <= self.radius

class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "Experimental Emergency Teleportation"
        self.input = self.getInput(self.day)

        self.make_image = False

        self.nanobots = {}

    def load_nanobots(self):
        self.nanobots = {}
        for i, line in enumerate(self.input.splitlines()):
            pos_string, r_string = line.split(', ')

            position = pos_string[5:-1].split(',')
            radius = int(r_string[2:])
            self.nanobots[i] = NanoBot(i, Point(int(position[0]), int(position[1]), int(position[2])), radius)

    def solve(self):
        start_time = time()

        self.load_nanobots()

        max_range_nanobot = max(self.nanobots.values(), key=lambda nanobot: nanobot.radius)
        part1 = len([bot for bot in self.nanobots.values() if max_range_nanobot.in_range(bot.position)])
        
        if self.make_image:
            img = self.image()
            img.save('solutions/2018/visuals/day23/img.png')

        min_x = min([bot.position.x for bot in self.nanobots.values()])
        min_y = min([bot.position.y for bot in self.nanobots.values()])
        min_z = min([bot.position.z for bot in self.nanobots.values()])
        
        max_x = max([bot.position.x for bot in self.nanobots.values()])
        max_y = max([bot.position.y for bot in self.nanobots.values()])
        max_z = max([bot.position.z for bot in self.nanobots.values()])

        # priority: -nrBots, distance, tie_breaker
        tie_breaker = 0
        queue = []
        heapq.heappush(queue, (0, 0, tie_breaker, Box(Point(min_x, min_y, min_z), Point(max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1)), list(self.nanobots.values())))
        final_point = None

        while len(queue) > 0:
            _, _, _, box, intersecting_bots = heapq.heappop(queue)

            # if tie_breaker % 1000 < 8:
            # print(len(intersecting_bots), box.size, box.distance(Point(0, 0, 0)), len(queue))

            if box.computed_size() == 1:
                final_point = box.min
                break

            for subBox in box.divide():
                new_intersecting_bots = [bot for bot in intersecting_bots if bot.intersects(subBox)]
                heapq.heappush(queue, (-len(new_intersecting_bots), subBox.distance(Point(0, 0, 0)), tie_breaker, subBox, new_intersecting_bots))
                # tie_breaker += 1

        part2 = final_point.distance(Point(0, 0, 0))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self):
        size = 1000
        min_x = min([bot.position.x for bot in self.nanobots.values()])
        max_x = max([bot.position.x for bot in self.nanobots.values()])
        min_y = min([bot.position.y for bot in self.nanobots.values()])
        max_y = max([bot.position.y for bot in self.nanobots.values()])

        diff_x = max_x - min_x
        diff_y = max_y - min_y

        x_frac = abs(min_x) / max_x
        y_frac = abs(min_y) / max_y

        x_factor = size / diff_x
        y_factor = size / diff_y

        factor = max(x_factor, y_factor)

        img = Image.new('RGB', (size, size), "black")
        pixels = img.load()
        for bot in self.nanobots.values():
            x = min(int(bot.position.x * factor) + int((size // 2) * x_frac), size - 1)
            y = min(int(bot.position.y * factor) + int((size // 2) * y_frac), size - 1)
            r = int(bot.radius * factor)

            print(x, y)
            pixels[x, y] = (255, 0, 0)
            for _x in range(x - r, x + r):
                for _y in range(y - r, y + r):
                    if _x < 0 or _x >= size or _y < 0 or _y >= size:
                        continue

                    if pixels[_x, _y][0] == 255:
                        continue

                    if self.distance((_x, _y, 0), (x, y, 0)) <= r:
                        current_color = pixels[_x, _y]
                        pixels[_x, _y] = (min(current_color[0] + 1, 255), min(current_color[1] + 1, 255), min(current_color[2] + 1, 255))
        return img

if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
