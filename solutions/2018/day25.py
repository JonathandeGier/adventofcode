from Table import Table
from time import time

class Point:
    def __init__(self, x: int, y: int, z: int, w: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.w - other.w)

    def __str__(self) -> str:
        return str((self.x, self.y, self.z, self.w))

class Constellation:
    def __init__(self, point: Point):
        self.points = [point]

    def fits_in_constellation(self, other_point: Point):
        return min([point.distance(other_point) for point in self.points]) <= 3

    def add_point(self, point: Point):
        self.points.append(point)

    def merge(self, other):
        for point in other.points:
            self.points.append(point)

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Four-Dimensional Adventure"
        self.input = self.getInput(self.day)

        self.points = []
        self.constellations = {}

    def load_points(self):
        self.points = []
        for line in self.input.splitlines():
            axis = line.split(',')
            self.points.append(Point(int(axis[0]), int(axis[1]), int(axis[2]), int(axis[3])))

    def find_constellations(self):
        for point in self.points:
            added_constellation = None
            constellations_to_remove = []
            for key in self.constellations:
                constellation = self.constellations[key]

                if constellation.fits_in_constellation(point) and added_constellation is None:
                    constellation.add_point(point)
                    added_constellation = constellation
                elif constellation.fits_in_constellation(point) and added_constellation is not None:
                    added_constellation.merge(constellation)
                    constellations_to_remove.append(key)
                    pass

            for key in constellations_to_remove:
                del self.constellations[key]

            if added_constellation is None:
                if len(self.constellations.keys()) == 0:
                    new_key = 0
                else:
                    new_key = max(self.constellations.keys()) + 1

                self.constellations[new_key] = Constellation(point)

    def solve(self):
        start_time = time()

        self.load_points()
        self.find_constellations()

        part1 = len(self.constellations.keys())
        part2 = "Trigger Underflow"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
