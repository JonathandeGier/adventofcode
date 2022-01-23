from getInput import get_input
from itertools import combinations

def get_packages():
    return [int(x) for x in get_input(2015, 24).splitlines()]

def product(items: list):
    product = 1
    for item in items:
        product *= item
    return product

def main():

    packages = get_packages()
    target = sum(packages) // 3

    i = 0
    while True:
        i += 1
        groups = []
        for group in combinations(packages, i):
            if sum(group) == target:
                groups.append(group)
        if len(groups) > 0:
            break

    group_lengths = [len(x) for x in groups]
    smallest_groups = []
    for group in groups:
        if len(group) == min(group_lengths):
            smallest_groups.append(group)

    quantum_entanglement = [product(x) for x in smallest_groups]
    
    print("Puzzle 1:")   
    print(min(quantum_entanglement))

    print("")

    target = sum(packages) // 4
    
    i = 0
    while True:
        i += 1
        groups = []
        for group in combinations(packages, i):
            if sum(group) == target:
                groups.append(group)
        if len(groups) > 0:
            break

    group_lengths = [len(x) for x in groups]
    smallest_groups = []
    for group in groups:
        if len(group) == min(group_lengths):
            smallest_groups.append(group)

    quantum_entanglement = [product(x) for x in smallest_groups]
    
    print("Puzzle 2:")
    print(min(quantum_entanglement))


if __name__ == "__main__":
    main()
