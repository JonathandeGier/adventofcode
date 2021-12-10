from getInput import get_input

def get_lines():
    return get_input(2015, 1)


def main():
    data = get_lines()
    final_floor = data.count("(") - data.count(")")
    
    print("Puzzle 1:")
    print("Final Floor: " + str(final_floor))

    print("")

    print("Puzzle 2:")
    floor = 0
    pos = 0
    for i, val in enumerate(data):
        if val == "(":
            floor += 1
        else:
            floor -= 1
        
        if floor == -1:
            pos = i + 1
            break
    print("Enter basement at: " + str(pos))


if __name__ == "__main__":
    main()
