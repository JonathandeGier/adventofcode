from collections import Counter
from itertools import count
from Table import Table
from time import time

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Chronal Coordinates"
        self.input = self.getInput(self.day)

    def get_coordinates(self):
        coords = {}
        for i, line in enumerate(self.input.splitlines()):
            xy = line.split(', ')
            coords[(int(xy[0]), int(xy[1]))] = i
        return coords

    def diff(self, a: int, b: int):
        return max(a, b) - min(a, b)

    def solve(self):
        start_time = time()

        coordinates = self.get_coordinates()
        
        minX = min(coordinates.keys(), key=lambda x: x[0])[0] - 1
        maxX = max(coordinates.keys(), key=lambda x: x[0])[0] + 1
        minY = min(coordinates.keys(), key=lambda x: x[1])[1] - 1
        maxY = max(coordinates.keys(), key=lambda x: x[1])[1] + 1

        closest_grid = {}
        all_closest_grid = {}
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                distances = [(coord[1], self.diff(coord[0][0], x) + self.diff(coord[0][1], y)) for coord in coordinates.items()]
                
                closest = min(distances, key=lambda x: x[1])
                equals = [distance for distance in distances if distance[1] == closest[1]]
                
                if len(equals) == 1:
                    closest_grid[(x, y)] = closest[0]

                distance_sum = sum([distance[1] for distance in distances])
                if distance_sum < 10000:
                    all_closest_grid[(x, y)] = 1
                else:
                    all_closest_grid[(x, y)] = 0

        # values on the edge will run out to infinity
        top_edge = [closest_grid[(x, minY)] for x in range(minX, maxX + 1) if (x, minY) in closest_grid]
        bottom_edge = [closest_grid[(x, maxY)] for x in range(minX, maxX + 1) if (x, maxY) in closest_grid]
        right_edge = [closest_grid[(maxX, y)] for y in range(minY, maxY + 1) if (maxX, y) in closest_grid]
        left_edge = [closest_grid[(minX, y)] for y in range(minY, maxY + 1) if (minX, y) in closest_grid]
        
        edge_values = set(top_edge + bottom_edge + right_edge + left_edge)

        areas = Counter(closest_grid.values()).most_common()
        
        i = 0
        biggest_area = areas[i]
        while biggest_area[0] in edge_values:
            i += 1
            biggest_area = areas[i]

        part1 = biggest_area[1]

        part2 = sum([val for val in all_closest_grid.values() if val == 1])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
