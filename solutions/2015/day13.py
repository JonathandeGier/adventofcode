from getInput import get_input
from itertools import permutations

def get_preferences():
    input = get_input(2015, 13).splitlines()
    preferences = {}
    names = []
    for line in input:
        segments = line[:len(line) - 1].split(" ")
        personA = segments[0]
        personB = segments[-1]
        amount = int(segments[3])
        if segments[2] == "lose":
            amount *= -1

        if personA not in preferences:
            preferences[personA] = {personB: amount}
            names.append(personA)
        else:
            preferences[personA][personB] = amount
    return preferences, names


def total_happiness(arrangement, preferences):
    total_happiness = 0
    for i, person in enumerate(arrangement):
        left = i - 1
        right = i + 1
        if right == len(arrangement):
            right = 0

        total_happiness += preferences[person][arrangement[left]]
        total_happiness += preferences[person][arrangement[right]]
    return total_happiness



def main():
    preferences, names = get_preferences()
    
    possebilities = list(permutations(names))
    
    max_happiness = 0
    for arrangement in possebilities:
        happiness = total_happiness(arrangement, preferences)
        if happiness > max_happiness:
            max_happiness = happiness

    print("Puzzle 1:")
    print("Hax Happiness: " + str(max_happiness))
    print("")

    me = "me"
    names.append(me)
    my_preferences = {}
    for person in preferences.keys():
        preferences[person][me] = 0
        my_preferences[person] = 0
    preferences[me] = my_preferences

    possebilities = list(permutations(names))
    
    max_happiness = 0
    for arrangement in possebilities:
        happiness = total_happiness(arrangement, preferences)
        if happiness > max_happiness:
            max_happiness = happiness

    print("Puzzle 2:")
    print("Hax Happiness with me: " + str(max_happiness))


if __name__ == "__main__":
    main()
