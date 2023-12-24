from Table import Table
from time import time

import re
from itertools import combinations
from z3 import *


class Hailstone:
    def __init__(self, x: int, y: int, z: int, vx: int, vy: int, vz: int):
        self.x = x
        self.y = y
        self.z = z

        self.vx = vx
        self.vy = vy
        self.vz = vz

        # 2d line equation parameters
        self.a = vy / vx

        diff_y = self.a * self.x
        self.b = self.y - diff_y


    def is_future(self, x: float, y: float) -> bool:
        assert self.vx != 0 and self.vy != 0

        if self.vx > 0:
            future_x = self.x < x
        else:
            future_x = self.x > x
        
        if self.vy > 0:
            future_y = self.y < y
        else:
            future_y = self.y > y
        
        return future_x and future_y


class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Never Tell Me The Odds"
        self.input = self.getInput(self.day)

        self.hailstones = []

    def parse_hailstones(self):
        self.hailstones = []
        for line in self.input.splitlines():
            groups = re.match('(-?\d+), +(-?\d+), +(-?\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)', line).groups()
            self.hailstones.append(Hailstone(int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4]), int(groups[5])))

    def intersects(self, stone1: Hailstone, stone2: Hailstone) -> bool:
        if stone1.a == stone2.a:
            # lines are parralel and will never intersect
            assert stone1.b != stone2.b, 'Lines are equal'
            return None

        x = (stone2.b - stone1.b) / (stone1.a - stone2.a)
        y = (stone1.a * x) + stone1.b

        return (x, y)


    def solve(self):
        start_time = time()

        self.parse_hailstones()
        
        _min = 200_000_000_000_000
        _max = 400_000_000_000_000

        part1 = 0
        for stone1, stone2 in combinations(self.hailstones, 2):
            # print(self.intersects3D(stone1, stone2))
            intersection = self.intersects(stone1, stone2)
            if intersection is None:
                # no intersection
                continue

            if intersection[0] < _min or intersection[0] > _max or intersection[1] < _min or intersection[1] > _max:
                # intersects outside area
                continue

            if not stone1.is_future(*intersection) or not stone2.is_future(*intersection):
                # doesn't collide in the future
                continue

            part1 += 1

        # 6 unknown variables we want to know (position + velocity in each dimension)
        x, y, z, vx, vy, vz = Ints('x y z vx vy vz')
        solver = Solver()
        for i, hailstone in enumerate(self.hailstones):
            # n unknowns for the time of intersection
            intersect = Int(f'i{i}')
            solver.add(intersect >= 0)

            # The position of the stone at the intersection time is the same as the position of the hailstone at the intersection time
            solver.add(x + intersect * vx == hailstone.x + intersect * hailstone.vx)
            solver.add(y + intersect * vy == hailstone.y + intersect * hailstone.vy)
            solver.add(z + intersect * vz == hailstone.z + intersect * hailstone.vz)

        solver.check()
        result = solver.model()

        part2 = result.eval(x + y + z).as_long()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
