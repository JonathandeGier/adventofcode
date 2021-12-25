from getInput import get_input

def get_grid():
    input = get_input(2021, 25).splitlines()
    grid = []
    for line in input:
        grid.append([x for x in line])

    return grid


def step(grid):
    width = len(grid[0])
    height = len(grid)

    moved = set()
    prev_occupied_1 = set()
    prev_occupied_2 = set()

    for row, row_data in enumerate(grid):
        for col, val in enumerate(row_data):
            if (row, col) in moved:
                continue
            if val == ">":
                next_location = col + 1
                if next_location == width:
                    next_location = 0
                if grid[row][next_location] == "." and (row, next_location) not in prev_occupied_1:
                    grid[row][next_location] = ">"
                    grid[row][col] = "."
                    moved.add((row, next_location))
                    prev_occupied_1.add((row, col))


    for row, row_data in enumerate(grid):
        for col, val in enumerate(row_data):
            if (row, col) in moved:
                continue
            if val == "v":
                next_location = row + 1
                if next_location == height:
                    next_location = 0
                if grid[next_location][col] == "." and (next_location, col) not in prev_occupied_2:
                    grid[next_location][col] = "v"
                    grid[row][col] = "."
                    moved.add((next_location, col))
                    prev_occupied_2.add((row, col))

    return grid, len(moved) > 0


def print_grid(grid, step):
    print(step)
    for row in grid:
        for val in row:
            print(val, end="", flush=True)
        print("")

    print("")


def main():
    grid = get_grid()

    steps = 0
    while True:
        grid, moved = step(grid)
        steps += 1
        if not moved:
            break

    print("Puzzle 1:")
    print(steps)

    print("")
    print("Puzzle 2:")
    print("Remotely start the Sleigh!")


if __name__ == "__main__":
    main()
