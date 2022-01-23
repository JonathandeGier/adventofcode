from getInput import get_input

def get_instructions():
    input = get_input(2015, 23)
    instructions = []

    for line in input.splitlines():
        instructions.append((line[:3].strip(), line[4:].strip()))

    return instructions


def run(instructions, registers):
    i = 0
    while True:
        if i >= len(instructions):
            break

        instruction = instructions[i]

        if instruction[0] == "inc":
            registers[instruction[1]] += 1
        elif instruction[0] == "hlf":
            registers[instruction[1]] = registers[instruction[1]] / 2
        elif instruction[0] == "tpl":
            registers[instruction[1]] = registers[instruction[1]] * 3
        elif instruction[0] == "jmp":
            i += int(instruction[1])
            continue
        elif instruction[0] == "jie":
            parts = instruction[1].split(",")
            reg = parts[0].strip()
            offset = parts[1].strip()

            if registers[reg] % 2 == 0:
                i += int(offset)
                continue
        elif instruction[0] == "jio":
            parts = instruction[1].split(",")
            reg = parts[0].strip()
            offset = parts[1].strip()

            if registers[reg] == 1:
                i += int(offset)
                continue

        i += 1

    return registers


def main():

    instructions = get_instructions()
    results = run(instructions, { "a": 0, "b": 0 })

    print("Puzzle 1:")
    print(results["b"])

    print("")

    results = run(instructions, { "a": 1, "b": 0 })

    print("Puzzle 2:")
    print(results["b"])


if __name__ == "__main__":
    main()
