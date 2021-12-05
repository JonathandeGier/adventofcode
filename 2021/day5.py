from getInput import get_input


def get_lines():
    input = get_input(2021, 5).splitlines()
    lines = []

    max_x = 0
    max_y = 0

    for entry in input:
        coordinates = entry.split(" -> ")
        line = []
        for coordinate in coordinates:
            x = int(coordinate.split(",")[0])
            y = int(coordinate.split(",")[1])

            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

            line.append([x, y])
        lines.append(line)
    
    return lines, max_x, max_y


def make_grid(x, y):
    grid = []
    for i in range(y + 1):
        row = []
        for j in range(x + 1):
            row.append(0)
        grid.append(row)
    
    return grid


def coordinates_of_line(line):
    coordinates = []
    x_steps = []
    y_steps = []

    if line[0][0] <= line[1][0]:
        for x in range(line[0][0], line[1][0] + 1, 1):
            x_steps.append(x)
    else:
        for x in range(line[0][0], line[1][0] - 1, -1):
            x_steps.append(x)

    if line[0][1] <= line[1][1]:
        for y in range(line[0][1], line[1][1] + 1, 1):
            y_steps.append(y)
    else:
        for y in range(line[0][1], line[1][1] - 1, -1):
            y_steps.append(y)

    if len(x_steps) == 1:
        x = x_steps[0]
        for y in y_steps:
            coordinates.append([x, y])
    elif len(y_steps) == 1:
        y = y_steps[0]
        for x in x_steps:
            coordinates.append([x, y])
    elif len(x_steps) == len(y_steps):
        for i, x in enumerate(x_steps):
            coordinates.append([x, y_steps[i]])
    else:
        print("Error in coordinates_of_line")

    return coordinates


def draw_line(line, grid):
    for coordinate in coordinates_of_line(line):
            grid[coordinate[1]][coordinate[0]] += 1


def calculate_crossings(grid):
    crossings = 0
    for row in grid:
        for value in row:
            if value > 1:
                crossings += 1
    return crossings


def main():
    lines, max_x, max_y = get_lines()

    print("Puzzle 1:")
    straight_lines = [x for x in lines if x[0][0] == x[1][0] or x[0][1] == x[1][1]]
    grid = make_grid(max_x, max_y)

    # draw lines
    for line in straight_lines:
        draw_line(line, grid)

    # calculate crossings
    crossings = calculate_crossings(grid)

    print("Crossings: " + str(crossings))
    print("")

    print("Puzzle 2:")

    # reset grid
    grid = make_grid(max_x, max_y)

    # draw lines
    for line in lines:
        draw_line(line, grid)

    # calculate crossings
    crossings = calculate_crossings(grid)

    print("Crossings: " + str(crossings))


if __name__ == "__main__":
    main()