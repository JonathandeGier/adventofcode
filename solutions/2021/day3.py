from getInput import get_input

input = get_input(2021, 3)

bitcounts = [
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
    {"1": 0, "0": 0},
]

for line in input.split("\n"):
    for i, bit in enumerate(line):
        bitcounts[i][bit] += 1

gamma_bits = ""
epsilon_bits = ""

for bitcount in bitcounts:
    if bitcount["1"] > bitcount["0"]:
        gamma_bits += "1"
        epsilon_bits += "0"
    else:
        gamma_bits += "0"
        epsilon_bits += "1"

gamma = int(gamma_bits, 2)
epsilon = int(epsilon_bits, 2)

print("Puzzle 1:")
print("gamma: " + str(gamma))
print("epsilon: " + str(epsilon))
print("power consumption: " + str(gamma * epsilon))
print("")

print("Puzzle 2:")

filtered_list = input.split("\n")
filtered_list = filtered_list[:len(filtered_list) - 1]

oxygen_bits = ""

for bitposition, not_used in enumerate(input.split("\n")[0]):
    bitcount = {
        "0": 0,
        "1": 0,
        "0_list": [],
        "1_list": []
    }

    for line in filtered_list:
        bitlist = list(line)
        bit = bitlist[bitposition]

        bitcount[bit] += 1

        if bit == "1":
            bitcount["1_list"].append(line)
        else:
            bitcount["0_list"].append(line)

    if bitcount["1"] >= bitcount["0"]:
        filtered_list = bitcount["1_list"]
    else:
        filtered_list = bitcount["0_list"]

    if len(filtered_list) == 1:
        oxygen_bits = filtered_list[0]
        break

oxygen = int(oxygen_bits, 2)
print("Oxygen: " + str(oxygen))

filtered_list = input.split("\n")
filtered_list = filtered_list[:len(filtered_list) - 1]

co2_bits = ""

for bitposition, not_used in enumerate(input.split("\n")[0]):
    bitcount = {
        "0": 0,
        "1": 0,
        "0_list": [],
        "1_list": []
    }

    for line in filtered_list:
        bitlist = list(line)
        bit = bitlist[bitposition]

        bitcount[bit] += 1

        if bit == "1":
            bitcount["1_list"].append(line)
        else:
            bitcount["0_list"].append(line)

    if bitcount["1"] < bitcount["0"]:
        filtered_list = bitcount["1_list"]
    else:
        filtered_list = bitcount["0_list"]

    if len(filtered_list) == 1:
        co2_bits = filtered_list[0]
        break

co2 = int(co2_bits, 2)
print("CO2: " + str(co2))

print("Life Support: " + str(oxygen * co2))