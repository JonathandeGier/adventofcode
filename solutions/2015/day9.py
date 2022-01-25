from itertools import permutations
from Table import Table
from time import time

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "All in a Single Night"
        self.input = self.getInput(self.day)

    def get_destinations(self):
        input = self.input.splitlines()
        locations = []
        distances = []
        for line in input:
            locdis = line.split(" = ")
            distance = int(locdis[1])
            location = locdis[0].split(" to ")

            if location[0] not in locations:
                locations.append(location[0])
            if location[1] not in locations:
                locations.append(location[1])

            location.append(distance)
            distances.append(location)
        return distances, locations

    def get_distance(self, loc1, loc2, distances):
        for distance in distances:
            if loc1 in distance and loc2 in distance:
                return distance[2]
        print("could not find distance")

    def solve(self):
        start_time = time()

        distances, locations = self.get_destinations()
        routes = list(permutations(locations))

        lowest_distance = 9999999999999999999999999999999999999999
        longest_distance = 0
        for route in routes:
            distance = 0
            for i in range(len(route) - 1):
                from_loc = route[i]
                to_loc = route[i + 1]
                distance += self.get_distance(from_loc, to_loc, distances)
            if distance < lowest_distance:
                lowest_distance = distance
            if distance > longest_distance:
                longest_distance = distance
                
        part1 = lowest_distance
        part2 = longest_distance

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
