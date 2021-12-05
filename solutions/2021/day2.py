from getInput import get_input

input = get_input(2021, 2)

distance = 0
depth = 0

for line in input.split("\n"):
    elements = line.split(" ")

    if len(elements) != 2:
        continue

    direction = elements[0]
    value = elements[1]

    if direction == 'forward':
        distance += int(value)
    if direction == 'down':
        depth += int(value)
    if direction == 'up':
        depth -= int(value)


print("Puzzle 1:")
print("depth: " + str(depth))
print("distance: " + str(distance))
print("answer: " + str(distance * depth))
print("")


distance = 0
depth = 0
aim = 0
for line in input.split("\n"):
    elements = line.split(" ")

    if len(elements) != 2:
        continue

    direction = elements[0]
    value = elements[1]

    if direction == 'forward':
        distance += int(value)
        depth += int(value) * aim
    if direction == 'down':
        aim += int(value)
    if direction == 'up':
        aim -= int(value)

print("Puzzle 2:")
print("depth: " + str(depth))
print("distance: " + str(distance))
print("answer: " + str(distance * depth))