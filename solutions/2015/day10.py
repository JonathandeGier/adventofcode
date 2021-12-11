from getInput import get_input
from itertools import groupby

def get_number():
    return get_input(2015, 10).strip()


def main():
    print("Puzzle 1:")
    number = get_number()
    for _ in range(40):
        next = ""
        seq = ["".join(g) for k, g in groupby(number)]
        for n in seq:
            next += str(len(n))
            next += n[0]
        number = next

    print("Length of number: " + str(len(number)))
    print("")

    print("Puzzle 2:")
    number = get_number()
    for _ in range(50):
        next = ""
        seq = ["".join(g) for k, g in groupby(number)]
        for n in seq:
            next += str(len(n))
            next += n[0]
        number = next
    print("Length of number: " + str(len(number)))


if __name__ == "__main__":
    main()
