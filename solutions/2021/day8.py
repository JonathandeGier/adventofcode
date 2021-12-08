from os import truncate
from typing import Counter, ForwardRef
from getInput import get_input

def get_digits():
    input = get_input(2021, 8).splitlines()
    digits = []
    for line in input:
        seq = line.split("|")[0]
        dig = line.split("|")[1]
        digits.append({"seq": seq.strip().split(" "), "dig": dig.strip().split(" ")})

    return digits


def remove_char(string: str, char):
    if char in string:
        return string[:string.index(char)] + string[string.index(char) + 1:]
    else:
        return string


def is_solved(mapping):
    for value in mapping.values():
        if len(value) > 1:
            return False
    return True

def almost_solved(mapping):
    if len(mapping["a"]) == 1 and len(mapping["b"]) == 1 and len(mapping["c"]) == 1 and len(mapping["d"]) == 2 and len(mapping["e"]) == 1 and len(mapping["f"]) == 1 and len(mapping["g"]) == 2:
        return True
    return False


def solve(mapping, digits):
    for digit in digits:
        pos = possebilities(digit, mapping)
        if len(pos) == 1:
            if pos[0] == 0:
                for letter in digit:
                    mapping["d"] = remove_char(mapping["d"], letter)
            if pos[0] == 1:
                for letter in digit:
                    mapping["a"] = remove_char(mapping["a"], letter)
                    mapping["b"] = remove_char(mapping["b"], letter)
                    mapping["d"] = remove_char(mapping["d"], letter)
                    mapping["e"] = remove_char(mapping["e"], letter)
                    mapping["g"] = remove_char(mapping["g"], letter)
            if pos[0] == 2:
                for letter in digit:
                    mapping["b"] = remove_char(mapping["b"], letter)
                    mapping["f"] = remove_char(mapping["f"], letter)
            if pos[0] == 3:
                for letter in digit:
                    mapping["b"] = remove_char(mapping["b"], letter)
                    mapping["e"] = remove_char(mapping["e"], letter)
            if pos[0] == 4:
                for letter in digit.split():
                    mapping["a"] = remove_char(mapping["a"], letter)
                    mapping["e"] = remove_char(mapping["e"], letter)
                    mapping["g"] = remove_char(mapping["g"], letter)
            if pos[0] == 5:
                for letter in digit:
                    mapping["c"] = remove_char(mapping["c"], letter)
                    mapping["e"] = remove_char(mapping["e"], letter)
            if pos[0] == 6:
                for letter in digit:
                    mapping["c"] = remove_char(mapping["c"], letter)
            if pos[0] == 7:
                for letter in digit.split():
                    mapping["b"] = remove_char(mapping["b"], letter)
                    mapping["d"] = remove_char(mapping["d"], letter)
                    mapping["e"] = remove_char(mapping["e"], letter)
                    mapping["g"] = remove_char(mapping["g"], letter)
            if pos[0] == 8:
                for letter in digit:
                    pass
            if pos[0] == 9:
                for letter in digit:
                    mapping["e"] = remove_char(mapping["e"], letter)


def possebilities(digit, mapping):
    if len(digit) == 2:
        return [1]
    elif len(digit) == 3:
        return [7]
    elif len(digit) == 4:
        return [4]
    elif len(digit) == 7:
        return [8]
    elif len(digit) == 5:
        possible = []
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["c"]) and contains_one_of(digit, mapping["d"]) and contains_one_of(digit, mapping["e"]) and contains_one_of(digit, mapping["g"]):
            possible.append(2)
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["c"]) and contains_one_of(digit, mapping["d"]) and contains_one_of(digit, mapping["f"]) and contains_one_of(digit, mapping["g"]):
            possible.append(3)
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["b"]) and contains_one_of(digit, mapping["d"]) and contains_one_of(digit, mapping["f"]) and contains_one_of(digit, mapping["g"]):
            possible.append(5)
        if len(possible) == 0:
            print("not possible")
        return possible
    elif len(digit) == 6:
        possible = []
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["b"]) and contains_one_of(digit, mapping["c"]) and contains_one_of(digit, mapping["e"]) and contains_one_of(digit, mapping["f"]) and contains_one_of(digit, mapping["g"]):
            possible.append(0)
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["b"]) and contains_one_of(digit, mapping["d"]) and contains_one_of(digit, mapping["e"]) and contains_one_of(digit, mapping["f"]) and contains_one_of(digit, mapping["g"]):
            possible.append(6)
        if contains_one_of(digit, mapping["a"]) and contains_one_of(digit, mapping["b"]) and contains_one_of(digit, mapping["c"]) and contains_one_of(digit, mapping["d"]) and contains_one_of(digit, mapping["f"]) and contains_one_of(digit, mapping["g"]):
            possible.append(9)
        if len(possible) == 0:
            print("not possible")
        # print(digit, possible)
        return possible
    else:
        print("not possible")
        return []
    

def contains_one_of(string, other_string) -> bool:
    for char in other_string:
        if char in string:
            return True
    return False


def mapping_one_possebility(mapping):
    for key in mapping.keys():
            if len(mapping[key]) == 1:
                for k in mapping.keys():
                    if key != k:
                        mapping[k] = remove_char(mapping[k], mapping[key])
    return mapping


def mapping_one_left(mapping):
    count = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "e": 0,
            "f": 0,
            "g": 0
        }
    for poss in mapping.values():
        for val in poss:
            count[val] += 1
    
    for key in count.keys():
        if count[key] == 1:
            for k in mapping.keys():
                if key in mapping[k]:
                    mapping[k] = key
    return mapping


def digit_to_number(digit, mapping):
    if mapping["a"] in digit and mapping["b"] in digit and mapping["c"] in digit and mapping["d"] not in digit and mapping["e"] in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 0
    elif mapping["a"] not in digit and mapping["b"] not in digit and mapping["c"] in digit and mapping["d"] not in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"] not in digit:
        return 1
    elif mapping["a"] in digit and mapping["b"] not in digit and mapping["c"] in digit and mapping["d"] in digit and mapping["e"] in digit and mapping["f"] not in digit and mapping["g"] in digit:
        return 2
    elif mapping["a"] in digit and mapping["b"] not in digit and mapping["c"] in digit and mapping["d"] in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 3
    elif mapping["a"] not in digit and mapping["b"] in digit and mapping["c"] in digit and mapping["d"] in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"]not in digit:
        return 4
    elif mapping["a"] in digit and mapping["b"] in digit and mapping["c"] not in digit and mapping["d"] in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 5
    elif mapping["a"] in digit and mapping["b"] in digit and mapping["c"] not in digit and mapping["d"] in digit and mapping["e"] in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 6
    elif mapping["a"] in digit and mapping["b"] not in digit and mapping["c"] in digit and mapping["d"] not in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"] not in digit:
        return 7
    elif mapping["a"] in digit and mapping["b"] in digit and mapping["c"] in digit and mapping["d"] in digit and mapping["e"] in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 8
    elif mapping["a"] in digit and mapping["b"] in digit and mapping["c"] in digit and mapping["d"] in digit and mapping["e"] not in digit and mapping["f"] in digit and mapping["g"] in digit:
        return 9
    else:
        return -1


def main():
    digits = get_digits()

    print("Puzzle 1:")
    count = 0
    for line in digits:
        for segment in line["dig"]:
            if len(segment) == 2 or len(segment) == 4 or len(segment) == 3 or len(segment) == 7:
                count += 1

    print("Nr. of 1, 4, 7 and 8 in the output digits: " + str(count))
    print("")

    print("Puzzle 2:")
    total = 0
    for line in digits:
        mapping = {
            "a": "abcdefg",
            "b": "abcdefg",
            "c": "abcdefg",
            "d": "abcdefg",
            "e": "abcdefg",
            "f": "abcdefg",
            "g": "abcdefg"
        }

        count = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "e": 0,
            "f": 0,
            "g": 0
        }

        one = ""
        seven = ""

        for digit in line["seq"]:
            for char in digit:
                count[char] += 1
            if len(digit) == 2:
                one = digit
            if len(digit) == 3:
                seven = digit
        
        # print(count)
        # print(Counter(count.values()))

        for char in seven:
            if char not in one:
                mapping["a"] = char

        for key in count.keys():
            if count[key] == 4:
                mapping["e"] = key
            if count[key] == 6:
                mapping["b"] = key
            if count[key] == 9:
                mapping["f"] = key

        # while not is_solved(mapping):
        for i in range(4):
            mapping = mapping_one_possebility(mapping)
            solve(mapping, line["seq"])
            mapping = mapping_one_left(mapping)

            if almost_solved(mapping):
                other_d = mapping["d"][1]
                mapping["d"] = mapping["d"][0]
                other_g = mapping["g"][0]
                mapping["g"] = mapping["g"][1]

                success = True
                for digit in line["seq"]:
                    if digit_to_number(digit, mapping) == -1:
                        success = False
                
                if success:
                    break

                mapping["d"] = other_d
                mapping["g"] = other_g

                success = True
                for digit in line["seq"]:
                    if digit_to_number(digit, mapping) == -1:
                        success = False
                
                if success:
                    break

                print("Mailed mapping")

        number = ""
        for digit in line["dig"]:
            number += str(digit_to_number(digit, mapping))

        total += int(number)
    print("Sum: " + str(total))
        


if __name__ == "__main__":
    main()
