from Table import Table
from time import time

class Point:
    def __init__(self, position: tuple, velocity: tuple):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "The Stars Align"
        self.input = self.getInput(self.day)
        self.closest_points = None

    def get_points(self):
        points = []
        for line in self.input.splitlines():
            position = (int(line[10:16]), int(line[17:24]))
            velocity = (int(line[36:38]), int(line[39:42]))

            points.append(Point(position, velocity))

        return points

    def get_bounds(self, points):
        min_x = min(points, key=lambda point: point.position[0]).position[0]
        max_x = max(points, key=lambda point: point.position[0]).position[0]

        min_y = min(points, key=lambda point: point.position[1]).position[1]
        max_y = max(points, key=lambda point: point.position[1]).position[1]

        return (min_x, max_x, min_y, max_y)

    def bound_score(self, points):
        bounds = self.get_bounds(points)

        return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2])

    def copy_points(self, points):
        new_points = []
        for point in points:
            new_points.append(Point(point.position, point.velocity))

        return new_points

    def print_points(self):
        bounds = self.get_bounds(self.closest_points)

        for y in range(bounds[2], bounds[3] + 1):
            for x in range(bounds[0], bounds[1] + 1):
                point = [point for point in self.closest_points if point.position == (x, y)]

                if len(point) == 0:
                    print(' ', end='')
                else:
                    print('#', end='')
            print('')

    def solve(self):
        start_time = time()

        points = self.get_points()
        closest_points = self.copy_points(points)
        seconds = 0

        while self.bound_score(points) <= self.bound_score(closest_points):
            closest_points = self.copy_points(points)
            seconds += 1
            
            for point in points:
                point.update()

        self.closest_points = closest_points

        part1 = "<display>"
        part2 = seconds - 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print('')
    day.print_points()
    print('')
