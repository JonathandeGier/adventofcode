from collections import deque
from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

ROOM = '.'
WALL = '#'
DOOR = '-'
UNKNOWN = '?'

NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "A Regular Map"
        self.input = self.getInput(self.day).strip()[1:-1]

        self.image_bounds = None
        self.make_video = True
        self.video = None

        # north = y--, east = x++, south = y++, west = x--
        self.map = {}

    def init_map(self):
        self.map = {}
        
        self.map[(-1, -1)] = WALL
        self.map[(-1, 0)] = UNKNOWN
        self.map[(-1, 1)] = WALL

        self.map[(0, -1)] = UNKNOWN
        self.map[(0, 0)] = ROOM
        self.map[(0, 1)] = UNKNOWN

        self.map[(1, -1)] = WALL
        self.map[(1, 0)] = UNKNOWN
        self.map[(1, 1)] = WALL

    def follow_regex(self, video_frame = False):
        i = 0
        position = (0, 0)
        stack = []
        while i < len(self.input):
            value = self.input[i]
            if value in DIRECTIONS:
                position = self.move(position, value)
            elif value == '(':
                stack.append(position)
            elif value == '|':
                position = stack[-1]
            elif value == ')':
                position = stack.pop()
            else:
                assert False, 'Unknown regex char: ' + value
            
            i += 1

            if video_frame:
                img = self.image()
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))


    def load_map(self):
        self.init_map()
        self.follow_regex()

        min_x = min([pos for pos in self.map.keys()], key=lambda x: x[0])[0]
        max_x = max([pos for pos in self.map.keys()], key=lambda x: x[0])[0]
        min_y = min([pos for pos in self.map.keys()], key=lambda x: x[1])[1]
        max_y = max([pos for pos in self.map.keys()], key=lambda x: x[1])[1]
        self.image_bounds = (min_x, max_x, min_y, max_y)

        img = self.image()
        img.save('solutions/2018/visuals/day20/maze.png')

        if self.make_video:
            self.init_map()

            img = self.image()
            self.video = cv2.VideoWriter('solutions/2018/visuals/day20/video.avi', 0, 120, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            self.follow_regex(True)

            cv2.destroyAllWindows()
            self.video.release()


    def move(self, position, direction):
        if direction == NORTH:
            self.map[position[0], position[1] - 1] = DOOR
            self.map[position[0], position[1] - 2] = ROOM

            if (position[0], position[1] - 3) not in self.map:
                self.map[position[0], position[1] - 3] = UNKNOWN
            
            if (position[0] + 1, position[1] - 2) not in self.map:
                self.map[position[0] + 1, position[1] - 2] = UNKNOWN
            
            if (position[0] - 1, position[1] - 2) not in self.map:
                self.map[position[0] - 1, position[1] - 2] = UNKNOWN

            self.map[position[0] + 1, position[1] - 3] = WALL
            self.map[position[0] - 1, position[1] - 3] = WALL

            return (position[0], position[1] - 2)

        elif direction == EAST:
            self.map[position[0] + 1, position[1]] = DOOR
            self.map[position[0] + 2, position[1]] = ROOM

            if (position[0] + 3, position[1]) not in self.map:
                self.map[position[0] + 3, position[1]] = UNKNOWN
            
            if (position[0] + 2, position[1] + 1) not in self.map:
                self.map[position[0] + 2, position[1] + 1] = UNKNOWN
            
            if (position[0] + 2, position[1] - 1) not in self.map:
                self.map[position[0] + 2, position[1] - 1] = UNKNOWN

            self.map[position[0] + 3, position[1] + 1] = WALL
            self.map[position[0] + 3, position[1] - 1] = WALL

            return (position[0] + 2, position[1])

        elif direction == SOUTH:
            self.map[position[0], position[1] + 1] = DOOR
            self.map[position[0], position[1] + 2] = ROOM

            if (position[0], position[1] + 3) not in self.map:
                self.map[position[0], position[1] + 3] = UNKNOWN
            
            if (position[0] + 1, position[1] + 2) not in self.map:
                self.map[position[0] + 1, position[1] + 2] = UNKNOWN
            
            if (position[0] - 1, position[1] + 2) not in self.map:
                self.map[position[0] - 1, position[1] + 2] = UNKNOWN

            self.map[position[0] + 1, position[1] + 3] = WALL
            self.map[position[0] - 1, position[1] + 3] = WALL

            return (position[0], position[1] + 2)

        elif direction == WEST:
            self.map[position[0] - 1, position[1]] = DOOR
            self.map[position[0] - 2, position[1]] = ROOM

            if (position[0] - 3, position[1]) not in self.map:
                self.map[position[0] - 3, position[1]] = UNKNOWN
            
            if (position[0] - 2, position[1] + 1) not in self.map:
                self.map[position[0] - 2, position[1] + 1] = UNKNOWN
            
            if (position[0] - 2, position[1] - 1) not in self.map:
                self.map[position[0] - 2, position[1] - 1] = UNKNOWN

            self.map[position[0] - 3, position[1] + 1] = WALL
            self.map[position[0] - 3, position[1] - 1] = WALL

            return (position[0] - 2, position[1])

        else:
            assert False, 'Unknown direction: ' + direction


    def solve(self):
        start_time = time()

        self.load_map()

        distances = {(0, 0): 0} # through number of doors
        queue = deque()
        queue.append((0, 0))
        while len(queue) > 0:
            position = queue.popleft()

            distance = distances[position]

            for direction in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if self.map[position[0] + direction[0], position[1] + direction[1]] != DOOR:
                    continue

                new_position = (position[0] + (direction[0] * 2), position[1] + (direction[1] * 2))
                if new_position in distances:
                    continue

                distances[new_position] = distance + 1
                queue.append(new_position)

        part1 = max(distances.values())
        part2 = len([distance for distance in distances.values() if distance >= 1000])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self):
        min_x = self.image_bounds[0]
        max_x = self.image_bounds[1]
        min_y = self.image_bounds[2]
        max_y = self.image_bounds[3]

        img = Image.new('RGB', (max_x - min_x + 1, max_y - min_y + 1), "black")
        pixels = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if (x + min_x, y + min_y) not in self.map:
                    pixels[x,y] = (0, 0, 0)
                elif x + min_x == 0 and y + min_y == 0:
                    pixels[x,y] = (0, 200, 0)
                elif self.map[x + min_x, y + min_y] == ROOM:
                    pixels[x,y] = (255, 255, 255)
                elif self.map[x + min_x, y + min_y] == DOOR:
                    pixels[x,y] = (255, 255, 255)
                elif self.map[x + min_x, y + min_y] == WALL:
                    pixels[x,y] = (0, 0, 0)
                else:
                    pixels[x,y] = (0, 0, 0)

        scale = 2
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.NEAREST)

        return img


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
