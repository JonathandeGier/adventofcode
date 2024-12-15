from Table import Table
from time import time

import cv2
from numpy import asarray

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Restroom Redoubt"
        self.input = self.getInput(self.day)

        self.max_x = 101
        self.max_y = 103

        self.make_visuals = __name__ == '__main__'

    def parse_robots(self):
        robots = []
        for line in self.input.splitlines():
            pos, vel = line.split(' ')
            pos = pos[2:]
            vel = vel[2:]

            pos_x, pos_y = pos.split(',')
            vel_x, vel_y = vel.split(',')

            robots.append({
                'pos': {'x': int(pos_x), 'y': int(pos_y)},
                'vel': {'x': int(vel_x), 'y': int(vel_y)},
            })
        return robots

    def solve(self):
        start_time = time()

        robots = self.parse_robots()

        for robot in robots:
            robot['pos']['x'] = (robot['pos']['x'] + (robot['vel']['x'] * 100)) % self.max_x
            robot['pos']['y'] = (robot['pos']['y'] + (robot['vel']['y'] * 100)) % self.max_y

        mid_x = self.max_x // 2
        mid_y = self.max_y // 2

        q1 = sum([1 for robot in robots if robot['pos']['x'] < mid_x and robot['pos']['y'] < mid_y])
        q2 = sum([1 for robot in robots if robot['pos']['x'] < mid_x and robot['pos']['y'] > mid_y])
        q3 = sum([1 for robot in robots if robot['pos']['x'] > mid_x and robot['pos']['y'] < mid_y])
        q4 = sum([1 for robot in robots if robot['pos']['x'] > mid_x and robot['pos']['y'] > mid_y])

        part1 = q1 * q2 * q3 * q4

        # assume the christmas tree is at least 5000 steps away
        for robot in robots:
            robot['pos']['x'] = (robot['pos']['x'] + (robot['vel']['x'] * 5000)) % self.max_x
            robot['pos']['y'] = (robot['pos']['y'] + (robot['vel']['y'] * 5000)) % self.max_y

        if self.make_visuals:
            img = self.image_robots(robots)
            img.save(self.visual_path('robots.png'))
            video = cv2.VideoWriter(self.visual_path('robots.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 30, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
        
        part2 = 0
        for frame in range(5101, 10000): # assume the christmas tree is seen within the first 10000 steps
            for robot in robots:
                robot['pos']['x'] = (robot['pos']['x'] + (robot['vel']['x'] * 1)) % self.max_x
                robot['pos']['y'] = (robot['pos']['y'] + (robot['vel']['y'] * 1)) % self.max_y

            # look for 25x25 square
            botmap = {}
            for robot in robots:
                botmap[robot['pos']['x'], robot['pos']['y']] = 'X'

            for pos in botmap.keys():
                is_square = True
                for i in range(25):
                    if (pos[0] + i, pos[1]) not in botmap:
                        is_square = False
                        break
                    if (pos[0], pos[1] + i) not in botmap:
                        is_square = False
                        break
                if is_square:
                    part2 = frame
                    break

            if is_square:
                break

            if self.make_visuals:
                img = self.image_robots(robots)
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))



        if self.make_visuals:
            img = self.image_robots(robots)
            img.save(self.visual_path('tree.png'))

            for _ in range(30 * 5):
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            
            video.release()
            cv2.destroyAllWindows()


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def image_robots(self, robots):
        data = {}
        for robot in robots:
            data[robot['pos']['x'], robot['pos']['y']] = 'X'

        return self.image_map(data, {'X': (255, 255, 255)}, bounds=(0, self.max_x, 0, self.max_y), scale=10)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
