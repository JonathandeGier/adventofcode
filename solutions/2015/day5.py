from getInput import get_input

def get_strings():
    return get_input(2015, 5).splitlines()

# Puzzle 1 conditions
def contains_vowels(string):
    a = string.count("a")
    e = string.count("e")
    i = string.count("i")
    o = string.count("o")
    u = string.count("u")
    return a + e + i + o + u >= 3

def contains_double(string):
    for i in range(len(string) - 1):
        if string[i] == string[i + 1]:
            return True
    return False

def does_not_contain(string):
    contains = "ab" in string or "cd" in string or "pq" in string or "xy" in string
    return not contains

# Puzzle 2 conditions
def contains_pair(string):
    for i in range(len(string) - 1):
        substr = string[i:i+2]
        if len(string.split(substr)) >= 3:
            return True
    return False

def contains_repeating_char(string):
    for i in range(len(string) - 2):
        if string[i] == string[i + 2]:
            return True
    return False

def main():
    print("Puzzle 1:")
    nice = 0
    for string in get_strings():
        if contains_vowels(string) and contains_double(string) and does_not_contain(string):
            nice += 1

    print("Nice strings: " + str(nice))
    print("")

    print("Puzzle 2:")
    nice = 0
    for string in get_strings():
        if contains_pair(string) and contains_repeating_char(string):
            nice += 1
    
    print("Nice strings: " + str(nice))


if __name__ == "__main__":
    main()
