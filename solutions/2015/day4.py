from getInput import get_input
import hashlib

def starts_with_5_zeros(string):
    return len(string) >= 5 and string[0] == "0" and string[1] == "0" and string[2] == "0" and string[3] == "0" and string[4] == "0"

def starts_with_6_zeros(string):
    return len(string) >= 6 and string[0] == "0" and string[1] == "0" and string[2] == "0" and string[3] == "0" and string[4] == "0" and string[5] == "0"

def main():
    key = get_input(2015, 4).strip()
    i = 0
    string = key + str(i)
    hash = hashlib.md5(string.encode()).hexdigest()

    while not starts_with_5_zeros(hash):
        i += 1
        string = key + str(i)
        hash = hashlib.md5(string.encode()).hexdigest()

    print("Puzzle 1:")
    print("lowest succesfull hash: " + str(i))
    print("Hash: " + hash)
    print("String: " + string)

    print("")

    while not starts_with_6_zeros(hash):
        i += 1
        string = key + str(i)
        hash = hashlib.md5(string.encode()).hexdigest()

    print("Puzzle 2:")
    print("lowest succesfull hash: " + str(i))
    print("Hash: " + hash)
    print("String: " + string)


if __name__ == "__main__":
    main()
