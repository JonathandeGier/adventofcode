from getInput import get_input

def get_lines():
    lines = get_input(2015, 2).splitlines()
    data = []
    for line in lines:
        row = []
        for length in line.split("x"):
            row.append(int(length))
        row.sort()
        data.append(row)

    return data


def main():
    data = get_lines()

    totalArea = 0
    totalRibbon = 0
    for present in data:
        area = (2 * present[0] * present[1]) + (2 * present[1] * present[2]) + (2 * present[0] * present[2]) + (present[0] * present[1])
        totalArea += area

        ribbon = (present[0] + present[0] + present[1] + present[1]) + (present[0] * present[1] * present[2])
        totalRibbon += ribbon

    print("Puzzle 1:")
    print("Area needed: " + str(totalArea))

    print("")

    print("Puzzle 2:")
    print("Ribbon needed: " + str(totalRibbon))


if __name__ == "__main__":
    main()
