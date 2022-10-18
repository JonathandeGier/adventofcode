from collections import defaultdict, deque
from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Reservoir Research"
        self.input = self.getInput(self.day)
        
        self.make_image = False
        self.video = None

        self.map = None
        self.bounds = None # tuple (min_x, max_x, min_y, max_y)

    def load_map(self):
        map = defaultdict(lambda: '.')
        for line in self.input.splitlines():
            min_x = None
            max_x = None
            min_y = None
            max_y = None

            fixed_val, range_val = line.split(', ')
            
            fixed_type, val = fixed_val.split('=')
            if fixed_type == 'x':
                min_x = int(val)
                max_x = int(val)
            elif fixed_type == 'y':
                min_y = int(val)
                max_y = int(val)
            else:
                assert False, 'unknown axis: ' + fixed_type

            range_type, _range = range_val.split('=')
            val_low, val_high = _range.split('..')
            if range_type == 'x':
                min_x = int(val_low)
                max_x = int(val_high)
            elif range_type == 'y':
                min_y = int(val_low)
                max_y = int(val_high)
            else:
                assert False, 'unknown axis: ' + range_type


            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    map[(x, y)] = '#'
            
        min_x = min([pos for pos in map.keys()], key=lambda x: x[0])[0]
        max_x = max([pos for pos in map.keys()], key=lambda x: x[0])[0]
        min_y = min([pos for pos in map.keys()], key=lambda x: x[1])[1]
        max_y = max([pos for pos in map.keys()], key=lambda x: x[1])[1]

        self.map = map
        self.bounds = (min_x, max_x, min_y, max_y)

    def in_bounds(self, position):
        return position[1] >= self.bounds[2] and position[1] <= self.bounds[3]


    def solve(self):
        start_time = time()

        self.load_map()

        if self.make_image:
            img = self.image()
            self.video = cv2.VideoWriter('solutions/2018/visuals/day17/video.avi', 0, 60, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            img.save('solutions/2018/visuals/day17/start.png')


        queue = deque()
        queue.append((500, self.bounds[2]))
        i = 0
        while len(queue) > 0:
            i += 1
            if self.make_image:
                img = self.image()
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            flow_layer = queue.popleft()

            if self.map[flow_layer] == '~':
                continue

            # 1: move down until encountering water or clay
            while self.map[(flow_layer[0], flow_layer[1] + 1)] in ['.', '|'] and self.in_bounds(flow_layer):
                self.map[flow_layer] = '|'
                flow_layer = (flow_layer[0], flow_layer[1] + 1)

            if not self.in_bounds(flow_layer):
                continue

            # 2: go left and right until encountering a wall or drain
            left_seeker = flow_layer
            while self.map[(left_seeker[0], left_seeker[1] + 1)] in ['#', '~'] and self.map[(left_seeker[0] - 1, left_seeker[1])] in ['.', '|']:
                left_seeker = (left_seeker[0] - 1, left_seeker[1])

            right_seeker = flow_layer
            while self.map[(right_seeker[0], right_seeker[1] + 1)] in ['#', '~'] and self.map[(right_seeker[0] + 1, right_seeker[1])] in ['.', '|']:
                right_seeker = (right_seeker[0] + 1, right_seeker[1])

            in_container = self.map[(left_seeker[0], left_seeker[1] + 1)] in ['#', '~'] and self.map[(right_seeker[0], right_seeker[1] + 1)] in ['#', '~']

            # 3: fill the row with values
            for x in range(left_seeker[0], right_seeker[0] + 1):
                if in_container:
                    self.map[(x, flow_layer[1])] = '~'
                else:
                    self.map[(x, flow_layer[1])] = '|'

            # 4: futher processing
            if in_container:
                # move the flow layer up by one 
                flow_layer = (flow_layer[0], flow_layer[1] - 1)
                queue.append(flow_layer)
            else:
                if self.map[(left_seeker[0], left_seeker[1] + 1)] in ['.', '|']:
                    queue.append(left_seeker)

                if self.map[(right_seeker[0], right_seeker[1] + 1)] in ['.', '|']:
                    queue.append(right_seeker)

        if self.make_image:
            img = self.image()
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            img.save('solutions/2018/visuals/day17/end.png')

            cv2.destroyAllWindows()
            self.video.release()

        # 33368 < x < ...
        part1 = sum([1 for item in self.map.items() if item[1] in ['~', '|'] and self.in_bounds(item[0])])
        part2 = sum([1 for item in self.map.items() if item[1] == '~' and self.in_bounds(item[0])])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self):
        img = Image.new('RGB', (self.bounds[1] - self.bounds[0] + 1, self.bounds[3] + 1), "black")
        pixels = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if self.map[(x + self.bounds[0], y)] == '.':
                    pixels[x,y] = (0, 0, 0)
                elif self.map[(x + self.bounds[0], y)] == '|':
                    pixels[x,y] = (0, 255, 0)
                elif self.map[(x + self.bounds[0], y)] == '~':
                    pixels[x,y] = (0, 0, 255)
                else:
                    pixels[x,y] = (255, 255, 255)

        return img


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
