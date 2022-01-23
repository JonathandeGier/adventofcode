from getInput import get_input

def get_location():
    input = get_input(2015, 25)
    words = input.split(" ")

    row = int(words[-3].strip()[:-1])
    column = int(words[-1].strip()[:-1])

    return (row, column)


def next(location):
    if location[0] == 1:
        return (location[1] + 1, 1)

    return (location[0] - 1, location[1] + 1)


def find(location: tuple, grid: dict):
    current = (1,1)

    while True:
        prev = current
        current = next(prev)

        grid[current] = (grid[prev] * 252533) % 33554393

        if current == location:
            return grid[current]


def main():

    location = get_location()
    grid = { (1,1): 20151125 }

    print("Puzzle 1:")
    print(find(location, grid))

    print("")

    print("Puzzle 2:")
    print("Start the machine!")


if __name__ == "__main__":
    main()
