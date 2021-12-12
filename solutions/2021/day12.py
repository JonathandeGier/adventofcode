from getInput import get_input
from collections import deque


def get_caves():
    input = get_input(2021, 12).splitlines()
    caves = {}
    vertices = []
    for line in input:
        v = line.split("-")
        if v[0] not in vertices:
            vertices.append(v[0])
        if v[1] not in vertices:
            vertices.append(v[1])

    for line in input:
        places = line.split("-")
        
        if places[0] not in caves:
            caves[places[0]] = [places[1]]
        else:
            caves[places[0]].append(places[1])

        if places[1] not in caves:
            caves[places[1]] = [places[0]]
        else:
            caves[places[1]].append(places[0])
    return caves


def solve(caves, p1):
    start = ("start", set(["start"]), None)
    possible_routes = 0
    Q = deque([start])
    while Q:
        pos, small, twice = Q.popleft()
        if pos == "end":
            possible_routes += 1
            continue
        for y in caves[pos]:
            if y not in small:
                new_small = set(small)
                if y.lower() == y:
                    new_small.add(y)
                Q.append((y, new_small, twice))
            elif y in small and twice is None and y not in ["start", "end"] and not p1:
                Q.append((y, small, y))
    return possible_routes


def main():
    caves = get_caves()

    print("Puzzle 1:")
    print("Possible routes: " + str(solve(caves, True)))
    print("")

    print("Puzzle 2:")
    print("Possible routes: " + str(solve(caves, False)))

if __name__ == "__main__":
    main()
