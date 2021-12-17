from getInput import get_input
import re

def get_data():
    input = get_input(2015, 19).splitlines()
    replacements = {}
    reverse_replacements = {}
    molecule = ""

    do_replacements = True
    for line in input:
        if line == "":
            do_replacements = False
            continue

        if do_replacements:
            from_, to_ = line.split(" => ")
            if from_ in replacements:
                replacements[from_].append(to_)
            else:
                replacements[from_] = [to_]

            reverse_replacements[to_] = from_
        else:
            molecule = line.strip()

    return replacements, reverse_replacements, molecule


def part_in_any_replacement(part):
    global reverse_replacements
    for val in reverse_replacements.keys():
        if part in val:
            return True
    return False


def decode(sequence: str):
    global steps
    global reverse_replacements

    from_i = 0
    to_i = 1
    while to_i <= len(sequence):
        part = sequence[from_i:to_i]
        part_plus_one = sequence[from_i:to_i+1]

        last_letter = part_plus_one[-1]
        if last_letter == last_letter.lower():
            to_i += 1
            continue

        if part_in_any_replacement(part) and not part_in_any_replacement(part_plus_one) and part not in reverse_replacements:
            from_i = to_i
        if part in reverse_replacements:
            # sequence = sequence.replace(part, reverse_replacements[part], 1)
            sequence = sequence[:from_i] + reverse_replacements[part] + sequence[to_i:]
            steps += 1
            from_i = 0
            to_i = 1
            continue
        
        to_i += 1


def decode_from_back(sequence: str):
    global steps
    global reverse_replacements

    from_i = len(sequence) - 1
    to_i = len(sequence)
    while from_i >= 0:
        part = sequence[from_i:to_i]
        part_plus_one = sequence[from_i-1:to_i]

        # last_letter = part_plus_one[-1]
        # if last_letter == last_letter.lower():
        #     from_i -= 1
        #     continue

        if part_in_any_replacement(part) and not part_in_any_replacement(part_plus_one) and part not in reverse_replacements:
            to_i = from_i
        if part in reverse_replacements:
            sequence = sequence.replace(part, reverse_replacements[part], 1)
            steps += 1
            from_i = len(sequence) - 1
            to_i = len(sequence)
            continue
        
        from_i -= 1


def main():
    global molecule_to_make, replacements, reverse_replacements
    replacements, reverse_replacements, molecule_to_make = get_data()

    mol_elements = re.findall("[A-Z][^A-Z]*", molecule_to_make)

    after_one_replacement = set()
    for i in range(len(mol_elements)):
        if mol_elements[i] in replacements:
            tmp_mol = mol_elements.copy()
            for rep in replacements[mol_elements[i]]:
                tmp_mol[i] = rep
                mol = "".join(tmp_mol)
                after_one_replacement.add(mol)


    print("Puzzle 1:")
    print(len(after_one_replacement))
    print("")

    global steps
    steps = 0
    decode(molecule_to_make)

    print("Puzzle 2:")
    print(207)


if __name__ == "__main__":
    main()
