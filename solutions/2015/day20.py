# from getInput import get_input

# def get_house_number():
#     return int(get_input(2015, 20).strip())

def presents_at_house(house: int):
    presents = 0
    print("checking " + str(house))
    for elf in range(1, house + 1):
        if house % elf == 0:
            presents += elf * 10
    return presents

def better_presents_at_house(house: int):
    result = sum([elf * 10 for elf in range(1, house + 1) if house % elf == 0])
    print("checking house " + str(house) + ": " + str(result))
    return result

def main():
    # house = get_house_number()
    house = 36000000

    # for h in range(1, 10):
    #     print(better_presents_at_house(h))
    better_presents_at_house(36000720)
    house_presents = better_presents_at_house(house)
    while True:
        house += 1
        presents = better_presents_at_house(house)
        if presents >= house_presents:
            break
    
    print("Puzzle 1:")
    # x < 36000600
    print(house)

    print("")

    print("Puzzle 2:")


if __name__ == "__main__":
    main()
