from getInput import get_input

def get_ingrediants():
    input = get_input(2015, 15).splitlines()
    ingrediants = []
    for line in input:
        segemnts = line.split(" ")
        capacity = int(segemnts[2][:len(segemnts[2]) - 1])
        durability = int(segemnts[4][:len(segemnts[4]) - 1])
        flavor = int(segemnts[6][:len(segemnts[6]) - 1])
        texture = int(segemnts[8][:len(segemnts[8]) - 1])
        calories = int(segemnts[10])
        ingrediants.append([capacity, durability, flavor, texture, calories])
    return ingrediants

# https://stackoverflow.com/questions/7748442/generate-all-possible-lists-of-length-n-that-sum-to-s-in-python
def percentages(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in percentages(length - 1, total_sum - value):
                yield (value,) + permutation

def calculate_score(ingrediants, percentages):
    property_scores = [0, 0, 0, 0]

    for i, percentage in enumerate(percentages):
        for j, property in enumerate(ingrediants[i]):
            if j == len(ingrediants[i]) - 1:
                continue
            property_scores[j] += (percentage * property)

    for i, val in enumerate(property_scores):
        if val < 0:
            property_scores[i] = 0

    return property_scores[0] * property_scores[1] * property_scores[2] * property_scores[3]

def calories(ingrediants, percentages):
    calories = 0

    for i, percentage in enumerate(percentages):
        calories += (percentage * ingrediants[i][4])
    
    return calories


def main():
    ingrediants = get_ingrediants()

    possebilities = list(percentages(len(ingrediants), 100))
    
    best_score = 0
    best_calories = 0
    for possebility in possebilities:
        score = calculate_score(ingrediants, possebility)
        if score > best_score:
            best_score = score

        if score > best_calories and calories(ingrediants, possebility) == 500:
            best_calories = score

    print("Puzzle 1:")
    print("Best score: " + str(best_score))
    print("")

    print("Puzzle 2:")
    print("Best caloties score: " + str(best_calories))


if __name__ == "__main__":
    main()
