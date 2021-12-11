from getInput import get_input

connections = {}
calcutated = {}

def get_connections():
    lines = get_input(2015, 7).splitlines()
    global connections
    connections = {}

    for instruction in lines:
        inout = instruction.split(" -> ")
        input = inout[0].split(" ")
        output = inout[1]

        if len(input) == 3:
            connections[output] = {
                "a": try_to_int(input[0]),
                "b": try_to_int(input[2]),
                "gate": input[1]
            }
            # print(connections[output])
        if len(input) == 2:
            connections[output] = {
                "a": try_to_int(input[1]),
                "b": '',
                "gate": input[0]
            }
            
        if len(input) == 1:
            connections[output] = {
                "a": try_to_int(input[0]),
                "b": '',
                "gate": ''
            }
    return connections


def try_to_int(value):
    try:
        return int(value)
    except Exception:
        return value

def get_output(wire):
    if isinstance(wire, int):
        return wire

    global connections
    global calcutated

    if wire in calcutated:
        return calcutated[wire]

    connection = connections[wire]

    if connection["gate"] == "AND":
        result = get_output(connection["a"]) & get_output(connection["b"])
        calcutated[wire] = result
        return result
    elif connection["gate"] == "OR":
        result = get_output(connection["a"]) | get_output(connection["b"])
        calcutated[wire] = result
        return result
    elif connection["gate"] == "NOT":
        result = ~ get_output(connection["a"])
        calcutated[wire] = result
        return result
    elif connection["gate"] == "LSHIFT":
        result = get_output(connection["a"]) << get_output(connection["b"])
        calcutated[wire] = result
        return result
    elif connection["gate"] == "RSHIFT":
        result = get_output(connection["a"]) >> get_output(connection["b"])
        calcutated[wire] = result
        return result
    else: # no gate
        if isinstance(connection["a"], int):
            calcutated[wire] = connection["a"]
            return connection["a"]
        else:
            return get_output(connection["a"])


def main():
    global connections
    global calcutated

    get_connections()
    print("Puzzle 1:")
    a = get_output("a")
    print("Output at a: " + str(a))

    print("")

    print("Puzzle 2:")
    connections["b"]["a"] = a
    calcutated = {}
    new_a = get_output("a")
    print("Output at a: " + str(new_a))


if __name__ == "__main__":
    main()
