from getInput import get_input
from itertools import permutations

def get_destinations():
    input = get_input(2015, 9).splitlines()
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


def get_distance(loc1, loc2, distances):
    for distance in distances:
        if loc1 in distance and loc2 in distance:
            return distance[2]
    print("could not find distance")


def main():
    distances, locations = get_destinations()
    routes = list(permutations(locations))

    lowest_distance = 9999999999999999999999999999999999999999
    longest_distance = 0
    for route in routes:
        distance = 0
        for i in range(len(route) - 1):
            from_loc = route[i]
            to_loc = route[i + 1]
            distance += get_distance(from_loc, to_loc, distances)
        if distance < lowest_distance:
            lowest_distance = distance
        if distance > longest_distance:
            longest_distance = distance
            
    print("Puzzle 1:")
    print("Lowest distance: " + str(lowest_distance))
    print("")
    print("Puzzle 2:")
    print("Longest distance: " + str(longest_distance))


if __name__ == "__main__":
    main()
