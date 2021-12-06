from getInput import get_input


def get_fish():
    input = get_input(2021, 6).split(",")
    input = [int(f.strip()) for f in input]
    fish = {}
    for i in range(9):
        fish[i] = len([f for f in input if f == i])
    return fish

def step_day(fish):
    new_fish = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }
    for life in fish.keys():
        if life > 0:
            new_fish[life - 1] += fish[life]
        else:
            new_fish[6] += fish[life]
            new_fish[8] += fish[life]

    return new_fish

def main():
    print("Puzzle 1:")
    fish = get_fish()
    
    for i in range(80):
        fish = step_day(fish)

    print("Count fish after 80 days: " + str(sum(fish.values())))
    print("")

    print("Puzzle 2:")
    fish = get_fish()
    
    for i in range(256):
        fish = step_day(fish)

    print("Count fish after 256 days: " + str(sum(fish.values())))


if __name__ == "__main__":
    main()
