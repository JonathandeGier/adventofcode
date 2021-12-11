from getInput import get_input

def get_instructions():
    input = get_input(2015, 6).splitlines()
    data = []
    for line in input:
        parts = line.split(" ")
        operation = parts[-4]
        from_coor = [int(x) for x in parts[-3].split(",")]
        to_coor = [int(x) for x in parts[-1].split(",")]
        data.append([operation, from_coor, to_coor])
    return data


def main():
    instructions = get_instructions()

    grid1 = []
    for _ in range(1000):
        row = []
        for _ in range(1000):
            row.append(False)
        grid1.append(row)

    grid2 = []
    for _ in range(1000):
        row = []
        for _ in range(1000):
            row.append(0)
        grid2.append(row)

    for instruction in instructions:
        for row in range(instruction[1][1], instruction[2][1] + 1):
            for column in range(instruction[1][0], instruction[2][0] + 1):
                if instruction[0] == "on":
                    grid1[row][column] = True
                    grid2[row][column] += 1
                elif instruction[0] == "off":
                    grid1[row][column] = False
                    if grid2[row][column] > 0:
                        grid2[row][column] -= 1
                elif instruction[0] == "toggle":
                    grid1[row][column] = not grid1[row][column]
                    grid2[row][column] += 2
                else:
                    print("Invalid operation")
    
    print("Puzzle 1:")
    on = 0
    for row in grid1:
        on += sum(row)

    print("Lights on: " + str(on))
    print("")

    print("Puzzle 2:")
    brightness = 0
    for row in grid2:
        brightness += sum(row)

    print("Lights on: " + str(brightness))


if __name__ == "__main__":
    main()
