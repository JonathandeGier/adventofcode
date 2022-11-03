from collections import deque
from Table import Table
from time import time
from PIL import Image

ROCKY = 0
WET = 1
NARROW = 2

TORCH = 'torch'
GEAR = 'gear'
NEITHER = 'neither'

POSSIBLE_TOOLS = {
    ROCKY: [GEAR, TORCH],
    WET: [GEAR, NEITHER],
    NARROW: [TORCH, NEITHER],
}

class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Mode Maze"
        self.input = self.getInput(self.day)

        self.depth = None
        self.target = None
        self.map = {}
        self.erotion_levels = {}

    def load_input(self):
        lines = self.input.splitlines()
        self.depth = int(lines[0].split(': ')[1])

        target = lines[1].split(': ')[1].split(',')
        self.target = tuple([int(val) for val in target])

    def build_map(self, extra = 0):
        self.map = {}
        self.erotion_levels = {}
        for x in range(self.target[0] + 1 + extra):
            for y in range(self.target[1] + 1 + extra):
                if x == 0 and y == 0:
                    geologic_index = 0
                elif x == self.target[0] and y == self.target[1]:
                    geologic_index = 0
                elif y == 0:
                    geologic_index = x * 16807
                elif x == 0:
                    geologic_index = y * 48271
                else:
                    geologic_index = self.erotion_levels[x-1, y] * self.erotion_levels[x, y-1]

                erosion_level = (geologic_index + self.depth) % 20183
                self.erotion_levels[x, y] = erosion_level

                self.map[x, y] = erosion_level % 3


    def solve(self):
        start_time = time()

        self.load_input()
        # self.depth = 510
        # self.target = (10, 10)
        
        self.build_map()

        img = self.image()
        img.save('solutions/2018/visuals/day22/map1.png')
        part1 = sum(self.map.values())
        
        # extend the map with a margin, so the quickest time can be found
        self.build_map(20)
        img = self.image()
        img.save('solutions/2018/visuals/day22/map2.png')

        time_map = {
            (0, 0): {
                TORCH: 0
            }
        }
        state = ((0, 0), TORCH, [(0, 0)])
        queue = deque()
        queue.append(state)

        found_path = None

        while len(queue) > 0:
            position, current_tool, path = queue.popleft()

            # save the path for a image
            if found_path == None and position == self.target and current_tool == TORCH:
                found_path = path

            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_position = (position[0] + direction[0], position[1] + direction[1])

                # make sure the new position is on the map
                if new_position not in self.map:
                    continue

                # make sure the new position is quicker than a already calculated route
                if new_position in time_map and current_tool in time_map[new_position] and time_map[new_position][current_tool] <= time_map[position][current_tool] + 1:
                    continue

                # make sure the new position is reachable with te current tool
                if current_tool not in POSSIBLE_TOOLS[self.map[new_position]]:
                    continue

                new_path = path.copy()
                new_path.append(new_position)

                if new_position not in time_map:
                    time_map[new_position] = {}

                time_map[new_position][current_tool] = time_map[position][current_tool] + 1

                queue.append((new_position, current_tool, new_path))

            for new_tool in POSSIBLE_TOOLS[self.map[position]]:
                if new_tool == current_tool:
                    continue

                # make sure the new position is quicker than a already calculated route
                if new_tool in time_map[position] and time_map[position][new_tool] <= time_map[position][current_tool] + 7:
                    continue

                time_map[position][new_tool] = time_map[position][current_tool] + 7
                
                queue.append((position, new_tool, path))

        part2 = time_map[self.target][TORCH]

        img = self.image(found_path)
        img.save('solutions/2018/visuals/day22/path.png')

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, path = []):
        max_x = max([pos for pos in self.map.keys()], key=lambda x: x[0])[0]
        max_y = max([pos for pos in self.map.keys()], key=lambda x: x[1])[1]

        img = Image.new('RGB', (max_x + 1, max_y + 1), "black")
        pixels = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if (x, y) not in self.map:
                    pixels[x,y] = (0, 0, 0)
                elif (x, y) in path:
                    pixels[x,y] = (199, 165, 2)   # yellow-gold ish
                elif self.map[x, y] == ROCKY:
                    pixels[x,y] = (140, 140, 140) # gray
                elif self.map[x, y] == WET:
                    pixels[x,y] = (120, 147, 173) # gray blue ish
                elif self.map[x, y] == NARROW:
                    pixels[x,y] = (60, 60, 60)    # dark gray
                else:
                    pixels[x,y] = (0, 0, 0)

        scale = 1
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.NEAREST)

        return img


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
