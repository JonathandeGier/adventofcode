from Table import Table
from time import time
import heapq

COLORS = {
    0: (20, 20, 20),
    1: (40, 40, 40),
    2: (60, 60, 60),
    3: (80, 80, 80),
    4: (100, 100, 100),
    5: (120, 120, 120),
    6: (140, 140, 140),
    7: (160, 160, 160),
    8: (180, 180, 180),
    9: (200, 200, 200),
    '*': (200, 200, 0),
}

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Clumsy Crucible"
        self.input = self.getInput(self.day)

        self.map = {}
        self.max_x = 0
        self.max_y = 0


    def parse_map(self):
        self.map = {}
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                self.map[(x, y)] = int(val)
        self.max_x = x
        self.max_y = y


    def path(self, start: tuple, end: tuple, part2: bool = False):
        queue = []
        visited = {}

        heapq.heappush(queue, (0, start, 0, 0, [start]))
        while queue:
            heat_loss, position, current_direction, direction_length, path = heapq.heappop(queue)

            # if we already visited this position in the same direction state with a lower heat loss, we can stop this path
            key = (position, current_direction, direction_length)
            if key in visited and visited[key] <= heat_loss:
                continue

            visited[key] = heat_loss

            # if we are are the end, we return
            if position == end:
                if part2 and direction_length < 4:
                    continue
                else:
                    return path, heat_loss

            
            for direction in ((0,-1), (1,0), (0,1), (-1,0)): # up, right, down, left
                new_position = (position[0] + direction[0], position[1] + direction[1])
                same_direction = direction == current_direction or len(path) == 1
                new_direction_length = direction_length + 1 if same_direction else 1

                # make sure the new position is not outside the map
                if new_position not in self.map:
                    continue

                # dont go back
                if len(path) >= 2 and path[-2] == new_position:
                    continue

                
                if part2:
                    # Part 2: go in a straight line for 4 to 10 blocks
                    if (not same_direction and direction_length < 4) or new_direction_length > 10:
                        continue
                else:
                    # Part 1: dont go straight 3 blocks in a row
                    if new_direction_length > 3:
                        continue


                new_heat_loss = heat_loss + self.map[new_position]
                if (new_position, direction, new_direction_length) not in visited:
                    new_path = path.copy()
                    new_path.append(new_position)
                    heapq.heappush(queue, (new_heat_loss, new_position, direction, new_direction_length, new_path))


        return ([], 0)


    def solve(self):
        start_time = time()

        self.parse_map()

        self.image_map(self.map, COLORS, scale=5).save(self.visual_path('map.png'))

        # Part 1
        path, heat_loss = self.path((0, 0), (self.max_x, self.max_y))
        part1 = heat_loss
        
        data = self.map.copy()
        for node in path:
            data[node] = '*'
        self.image_map(data, COLORS, scale=5).save(self.visual_path('part1.png'))

        # Part 2
        path, heat_loss = self.path((0, 0), (self.max_x, self.max_y), True)
        part2 = heat_loss
        
        data = self.map.copy()
        for node in path:
            data[node] = '*'
        self.image_map(data, COLORS, scale=5).save(self.visual_path('part2.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
