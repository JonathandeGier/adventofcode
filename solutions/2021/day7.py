from getInput import get_input


def get_positions():
    input = get_input(2021, 7).split(",")
    return [int(i) for i in input]


def align(positions, target):
    fuel = 0
    for value in positions:
        fuel += abs(value - target)
    return fuel


def align2(positions, target):
    fuel = 0
    for value in positions:
        fuel += calculate_fuel(abs(value - target))
    return fuel


def calculate_fuel(distance):
    return int(((distance * distance) + distance) / 2)


def main():
    print("Puzzle 1:")
    positions = get_positions()

    fuel_cost = {}
    for i in range(min(positions), max(positions) + 1):
        fuel_cost[align(positions, i)] = i

    min_fuel = min(fuel_cost.keys())
    print("Lowest fuel cost: " + str(min_fuel) + " to position " + str(fuel_cost[min_fuel]))
    print("")

    print("Puzzle 2:")
    fuel_cost = {}
    for i in range(min(positions), max(positions) + 1):
        fuel_cost[align2(positions, i)] = i

    min_fuel = min(fuel_cost.keys())
    print("Lowest fuel cost: " + str(min_fuel) + " to position " + str(fuel_cost[min_fuel]))


if __name__ == "__main__":
    main()
