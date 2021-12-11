from getInput import get_input

def get_password():
    return get_input(2015, 11).strip()


def increment(string: str, index = -1):
    try:
        char = string[index]
    except IndexError:
        return "a" + string

    next_char = next_alpha(char)
    
    s = list(string)
    s[index] = next_char
    string = "".join(s)
    
    if next_char == "a":
        string = increment(string, index - 1)

    return string

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65).lower()


def has_incrementing_straight(string: str):
    for i in range(len(string) - 2):
        char0 = ord(string[i])
        char1 = ord(string[i + 1])
        char2 = ord(string[i + 2])

        if char1 - char0 == 1 and char2 - char1 == 1:
            return True
    return False

def does_not_contain_illegal_letters(string: str):
    if "i" in string or "o" in string or "l" in string:
        return False
    return True

def contains_non_overlapping_pair(string: str):
    for i in range(len(string) - 1):
        char0 = string[i]
        char1 = string[i + 1]
        
        if char0 == char1 and i + 3 <= len(string) - 1:
            substr = string[i + 2:]
            for j in range(len(substr) - 1):
                char2 = substr[j]
                char3 = substr[j + 1]

                if char2 == char3:
                    return True
    return False

def valid_password(string):

    return has_incrementing_straight(string) and does_not_contain_illegal_letters(string) and contains_non_overlapping_pair(string)


def main():
    password = get_password()

    print("Puzzle 1:")

    while not valid_password(password):
        password = increment(password)

    print("Valid Password: " + password)
    print("")

    print("Puzzle 2:")
    password = increment(password)
    while not valid_password(password):
        password = increment(password)
    
    print("Next valid Password: " + password)


if __name__ == "__main__":
    main()
