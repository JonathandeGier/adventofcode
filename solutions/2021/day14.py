from typing import Counter
from getInput import get_input

def get_data():
    input = get_input(2021, 14).splitlines()
    seed = ""
    insertions = {}
    for line in input:
        if seed == "":
            seed = line.strip()
            continue
        if line == "":
            continue

        parts = line.split(" -> ")
        insertions[parts[0]] = parts[1]
        
    return seed, insertions


def main():
    seed, insertions = get_data()

    for _ in range(10):
        new_seed = seed[0]
        for i in range(len(seed) - 1):
            part = seed[i:i+2]
            new_seed += insertions[part] + part[1]
        seed = new_seed

    count = Counter(seed)
    minn = min(count.values())
    maxx = max(count.values())

    print("Puzzle 1:")
    print("Answer: " + str(maxx - minn))
    print("")

    seed, insertions = get_data()

    
    counter = Counter()
    for i in range(len(seed)-1):
        counter[seed[i]+seed[i+1]] += 1

    for t in range(40):
        # If AB->R, then AB becomes (AR, RB)
        temp_counter = Counter()
        for k in counter:
            temp_counter[k[0]+insertions[k]] += counter[k]
            temp_counter[insertions[k]+k[1]] += counter[k]
        counter = temp_counter

    # char_count = {character: how many times that character appears}
    char_count = Counter()
    # Most letters are both the first letter *and* the second letter of a pair.
    # If we take the first letter of each pair, we count every character except the last one.
    # But the last character is the same as the last character of the original string!
    # We never add characters to the end.
    # So just add that.
    for k in counter:
        char_count[k[0]] += counter[k]
    char_count[seed[-1]] += 1

    print("Puzzle 2:")
    print("Answer: " + str(max(char_count.values())-min(char_count.values())))


if __name__ == "__main__":
    main()
