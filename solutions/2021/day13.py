from getInput import get_input

def get_data():
    input = get_input(2021, 13).splitlines()
    dots = set()
    folds = []
    D = True
    for line in input:
        if line == "":
            D = False
            continue

        if D:
            dot = [int(x) for x in line.split(",")]
            x = int(line.split(",")[0])
            y = int(line.split(",")[1])
            dots.add((x, y))
        else:
            segments = line.split(" ")[2].split("=")
            if segments[0] == "x":
                folds.append([int(segments[1]), 0])
            else:
                folds.append([0, int(segments[1])])
    return dots, folds


def fold(dots: set, foldline):
    new_dots = set()

    if foldline[1] == 0: # fold along x
        x = foldline[0]
        for dot in dots:
            if dot[0] > x:
                new_x = dot[0] - ((dot[0] - x) * 2)
                new_dots.add((new_x, dot[1]))
            else:
                new_dots.add(dot)
    else: # fold along y
        y = foldline[1]
        for dot in dots:
            if dot[1] > y:
                new_y = dot[1] - ((dot[1] - y) * 2)
                new_dots.add((dot[0], new_y))
            else:
                new_dots.add(dot)

    return new_dots


def main():
    dots, folds = get_data()

    dots1 = fold(dots, folds[0])

    print("Puzzle 1:")
    print("Dots after the first fold: " + str(len(dots1)))
    print("")

    for _fold in folds:
        dots = fold(dots, _fold)

    print("Puzzle 2:")

    xx = [cor[0] for cor in dots]
    yy = [cor[1] for cor in dots]

    for y in range(min(yy), max(yy) + 1):
        for x in range(min(xx), max(xx) + 1):
            if (x, y) in dots:
                print("#", end="", flush=True)
            else:
                print(".", end="", flush=True)
        print("\n", end="", flush=True)
    
    print("Answer: HEJHJRCJ")


if __name__ == "__main__":
    main()
