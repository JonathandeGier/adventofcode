from getInput import get_input
import ast

def get_strings():
    input = get_input(2015, 8).splitlines()
    return input

def len_in_code(string):
    return len(string)

def len_chars(string):
    return len(ast.literal_eval(string))

def len_encoded(string: str):
    new_string = '"'
    for char in string:
        if char == "\\" or char == '"':
            new_string += "\\"
        new_string += char
    new_string += '"'

    return len(new_string)

def main():
    strings = get_strings()

    answer = 0
    for string in strings:
        answer += len_in_code(string)
        answer -= len_chars(string)

    print("Puzzle 1:")
    print("Answer: " + str(answer))

    print("")

    answer = 0
    for string in strings:
        answer += len_encoded(string)
        answer -= len_in_code(string)

    print("Puzzle 2:")
    print("Answer: " + str(answer))


if __name__ == "__main__":
    main()
