from getInput import get_input
import json

def get_data():
    return json.loads(get_input(2015, 12))


def deep_sum(item):
    if type(item) == int:
        return item
    if type(item) == str:
        return 0

    sum = 0
    if type(item) == dict:
        for subItem in item.values():
            sum += deep_sum(subItem)
    for subItem in item:
            sum += deep_sum(subItem)
    return sum


def deep_sum_no_red(item):
    if type(item) == int:
        return item
    if type(item) == str:
        return 0

    sum = 0
    if type(item) == dict:
        for val in item.values():
            if type(val) == str and val == "red":
                return 0

        for subItem in item.values():
            sum += deep_sum_no_red(subItem)
    for subItem in item:
            sum += deep_sum_no_red(subItem)
    return sum


def main():
    data = get_data()
    total = deep_sum(data)

    print("Puzzle 1:")
    print("Sum: " + str(total))

    print("")

    total = deep_sum_no_red(data)

    print("Puzzle 2:")
    print("Sum: " + str(total))


if __name__ == "__main__":
    main()
