from Table import Table
from time import time
import heapq

import cv2
from numpy import asarray

class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position: tuple=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Day18(Table):

    def __init__(self):
        self.day = 18
        self.title = "RAM Run"
        self.input = self.getInput(self.day)

        self.map = {}
        self.breakpoint = 1024
        self.max_axis = 70
        
        self.make_visuals = __name__ == '__main__'
        # self.make_visuals = False

    def astar(self, start: tuple, end: tuple, make_video = False, with_heuristic = True):
        start_node = Node(None, start)
        end_node = Node(None, end)

        video = None
        if make_video:
            img = self.image()
            video = cv2.VideoWriter(self.visual_path('path.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 30, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        queue = []
        visited = {}

        heapq.heappush(queue, (0, start, start_node))

        while len(queue) > 0:

            # get node with lowest cost
            length, _, current_node = heapq.heappop(queue)

            if current_node.position in visited and visited[current_node.position] <= length:
                continue

            visited[current_node.position] = length

            if make_video:
                img = self.image([], visited.keys())
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            # check if the current node is the end node and return the path if so
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                    if make_video:
                        img = self.image(path, visited.keys())
                        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

                # video stuff
                if make_video:
                    img = self.image(path, visited.keys())
                    for _ in range(150):
                        video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
                    
                    video.release()
                    cv2.destroyAllWindows()

                return path[::-1]

            # generate next possible directions
            directions = []
            for position_difference in [(0, 1), (0, -1), (-1, 0), (1, 0)]: # up, down, left, right
                new_position = (current_node.position[0] + position_difference[0], current_node.position[1] + position_difference[1])

                if new_position in self.map:
                    # print('not in map:', new_position)
                    continue

                if new_position[0] < 0 or new_position[0] > self.max_axis or new_position[1] < 0 or new_position[1] > self.max_axis:
                    continue


                new_node = Node(current_node, new_position)
                directions.append(new_node)

            for direction in directions:

                direction.g = current_node.g + 1
                direction.h = ((direction.position[0] - end_node.position[0]) ** 2) + ((direction.position[1] - end_node.position[1]) ** 2)
                direction.f = direction.g
                if with_heuristic:
                    direction.f += direction.h

                if direction.position not in visited or visited[direction.position] > direction.h:
                    heapq.heappush(queue, (direction.f, direction.position, direction))

        if make_video:
            video.release()
            cv2.destroyAllWindows()

        # No path found
        return False

    def solve(self):
        start_time = time()

        bitstream = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in self.input.splitlines()]

        for pos in bitstream[:1024]:
            self.map[pos] = '#'

        path = self.astar((0 ,0), (self.max_axis, self.max_axis), make_video=self.make_visuals, with_heuristic=False)
        part1 = len(path) - 1

        if self.make_visuals:
            img = self.image()
            img.save(self.visual_path('map.png'))
            video = cv2.VideoWriter(self.visual_path('part2.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 30, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        # Optimization: binary search
        part2 = "None"
        for pos in bitstream[1024:]:
            self.map[pos] = '#'
            
            path = self.astar((0, 0), (self.max_axis, self.max_axis))
            if path == False:
                part2 = ','.join([str(x) for x in pos])
                break

            if self.make_visuals:
                img = self.image(path, path)
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        if self.make_visuals:
            for _ in range(150):
                video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            video.release()
            cv2.destroyAllWindows()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def image(self, path: list = [], highlight = []):
        data = self.map.copy()
        
        for pos in highlight:
            data[pos] = 'o'
        for pos in path:
            data[pos] = 'O'

        return self.image_map(data, {'#': (255, 255, 255), 'O': (0, 255, 0), 'o': (50, 50, 100)}, scale=10, bounds=(0, self.max_axis, 0, self.max_axis))


if __name__ == "__main__":
    day = Day18()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
