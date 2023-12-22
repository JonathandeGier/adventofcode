from Table import Table
from time import time
from collections import defaultdict
import heapq

class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Sand Slabs"
        self.input = self.getInput(self.day)

        self.bricks = []

    def parse_bricks(self):
        self.bricks = []
        for line in self.input.splitlines():
            start, end = line.split('~')
            start = tuple([int(val) for val in start.split(',')])
            end = tuple([int(val) for val in end.split(',')])
            
            # assert the start corner is lower than the end corner
            assert start[0] <= end[0]
            assert start[1] <= end[1]
            assert start[2] <= end[2]

            self.bricks.append((start, end))


    def on_floor(self, brick: tuple) -> bool:
        return min(brick[0][2], brick[1][2]) == 1


    def move_down(self, brick: tuple) -> tuple:
        if self.on_floor(brick):
            # brick is already on the floor
            return brick
        
        new_start = (brick[0][0], brick[0][1], brick[0][2] - 1)
        new_end = (brick[1][0], brick[1][1], brick[1][2] - 1)

        return (new_start, new_end)

    def move_up(self, brick: tuple) -> tuple:
        new_start = (brick[0][0], brick[0][1], brick[0][2] + 1)
        new_end = (brick[1][0], brick[1][1], brick[1][2] + 1)

        return (new_start, new_end)


    def collides(self, brick: tuple, origional_brick: tuple) -> bool:
        for other_brick in self.bricks:
            if other_brick == origional_brick:
                continue

            if self.overlaps(brick, other_brick):
                return True
            
        return False


    def overlaps(self, brick: tuple, other_brick: tuple) -> bool:
        return self.overlaps_line(brick[0][0], brick[1][0], other_brick[0][0], other_brick[1][0]) and \
            self.overlaps_line(brick[0][1], brick[1][1], other_brick[0][1], other_brick[1][1]) and \
            self.overlaps_line(brick[0][2], brick[1][2], other_brick[0][2], other_brick[1][2])

    def overlaps_line(self, brick_1_start: int, brick_1_end: int, brick_2_start: int, brick_2_end: int) -> tuple:
        return brick_1_end >= brick_2_start and brick_2_end >= brick_1_start


    def solve(self):
        start_time = time()

        self.parse_bricks()

        # Drop all the bricks
        bricks_to_drop = sorted(self.bricks, key=lambda brick: min(brick[0][2], brick[1][2]))
        for brick in bricks_to_drop:
            new_brick = brick
            while True:
                if self.on_floor(new_brick):
                    break

                possible_brick = self.move_down(new_brick)
                if self.collides(possible_brick, brick):
                    break

                new_brick = possible_brick
            
            # print(f'Dropping {brick} to {new_brick}')
            i = self.bricks.index(brick)
            self.bricks[i] = new_brick

        # a brick can be removed if the bricks it is supporting is supported by more than 1 brick
        supporting = defaultdict(list)
        supported_by = defaultdict(list)
        for brick in self.bricks:
            lower = self.move_down(brick)
            upper = self.move_up(brick)

            on_floor = self.on_floor(brick)
            if on_floor:
                supporting['floor'].append(brick)

            for other_brick in self.bricks:
                if other_brick == brick:
                    continue
                
                if not on_floor and self.overlaps(lower, other_brick):
                    supported_by[brick].append(other_brick)

                if self.overlaps(upper, other_brick):
                    supporting[brick].append(other_brick)

        part1 = 0
        for brick in self.bricks:
            can_drop = True
            for upper_brick in supporting[brick]:
                if len(supported_by[upper_brick]) == 1:
                    can_drop = False
                    break

            if can_drop:
                part1 += 1


        part2 = 0
        for brick in self.bricks:
            would_fall = set()

            queue = []
            for upper_brick in supporting[brick]:
                if len(supported_by[upper_brick]) == 1:
                    would_fall.add(upper_brick)
                    heapq.heappush(queue, (min(upper_brick[0][2], upper_brick[1][2]), upper_brick))

            while queue:
                _, linked_brick = heapq.heappop(queue)
                for upper_brick in supporting[linked_brick]:
                    if all([s_linked_brick in would_fall for s_linked_brick in supported_by[upper_brick]]):
                        would_fall.add(upper_brick)
                        heapq.heappush(queue, (min(upper_brick[0][2], upper_brick[1][2]), upper_brick))

            part2 += len(would_fall)


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
