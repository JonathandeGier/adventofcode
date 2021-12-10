from getInput import get_input

def get_data():
    input = get_input(2021, 10).splitlines()
    return input


def main():
    lines = get_data()
    corrupt_score = 0
    completion_scores = []
    for line in lines:
        chars = []
        for char in line:
            if char in "([{<":
                chars.append(char)
                continue
            if (chars[-1] == "(" and char == ")") or (chars[-1] == "[" and char == "]") or (chars[-1] == "{" and char == "}") or (chars[-1] == "<" and char == ">"):
                chars.pop()
                continue

            # illegal character check
            if char == ")":
                corrupt_score += 3
                chars = []
                break
            if char == "]":
                corrupt_score += 57
                chars = []
                break
            if char == "}":
                corrupt_score += 1197
                chars = []
                break
            if char == ">":
                corrupt_score += 25137
                chars = []
                break
            
        temp_score = 0
        while len(chars) > 0:
            temp_score *= 5
            if chars[-1] == "(":
                temp_score += 1
            elif chars[-1] == "[":
                temp_score += 2
            elif chars[-1] == "{":
                temp_score += 3
            elif chars[-1] == "<":
                temp_score += 4
            chars.pop()

        if temp_score != 0:
            completion_scores.append(temp_score)

            


    print("Puzzle 1:")
    print("Corrupt Score: " + str(corrupt_score))

    print("")

    print("Puzzle 2:")
    completion_scores.sort()
    print("Completion Score: " + str(completion_scores[int(len(completion_scores) / 2)]))


if __name__ == "__main__":
    main()
