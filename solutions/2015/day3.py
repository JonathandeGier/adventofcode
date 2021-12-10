from getInput import get_input

def get_data():
    return get_input(2015, 3)


def main():

    visited = {
        "0,0": 1
    }

    x = 0
    y = 0
    for char in get_data():
        if char == "^":
            y += 1
        if char == "v":
            y -= 1
        if char == "<":
            x -= 1
        if char == ">":
            x += 1

        location = str(x) + "," + str(y)
        if location not in visited:
            visited[location] = 1
        else:
            visited[location] += 1
        
    multiple_visits = 0
    for count in visited.values():
        if count >= 1:
            multiple_visits += 1

    print("Puzzle 1:")
    print("Visited houses: " + str(multiple_visits))

    print("")

    visited = {
        "0,0": 2
    }

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    for i, char in enumerate(get_data()):
        if i % 2 == 0:
            if char == "^":
                y1 += 1
            if char == "v":
                y1 -= 1
            if char == "<":
                x1 -= 1
            if char == ">":
                x1 += 1

            location = str(x1) + "," + str(y1)
            if location not in visited:
                visited[location] = 1
            else:
                visited[location] += 1
        if i % 2 != 0:
            if char == "^":
                y2 += 1
            if char == "v":
                y2 -= 1
            if char == "<":
                x2 -= 1
            if char == ">":
                x2 += 1
            
            location = str(x2) + "," + str(y2)
            if location not in visited:
                visited[location] = 1
            else:
                visited[location] += 1
        
    multiple_visits = 0
    for count in visited.values():
        if count >= 1:
            multiple_visits += 1

    print("Puzzle 2:")
    print("Visited houses: " + str(multiple_visits))


if __name__ == "__main__":
    main()
