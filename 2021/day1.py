from getInput import get_input

input = get_input(2021, 1)

array = []
for line in input.split("\n"):
    stripped = line.strip()
    if len(stripped) != 0:
        array.append(int(line.strip()))


increased = 0
decreased = 0
last = 1111111111111111111111111111111
for value in array:
    if (value < last):
        decreased += 1
    else:
        increased += 1
    last = value

print("")
print("")

print("Puzzle 1:")
print("Increased: ")
print(increased)

print("Decreased: ")
print(decreased)
print("")

condensed = []

for i, value in enumerate(array):
    if i < 2:
        continue

    new_value = array[i-2] + array[i-1] + array[i]
    condensed.append(new_value)


increased = 0
same = 0
decreased = 0
last = 1111111111111111111111111111111
for value in condensed:
    if (value < last):
        decreased += 1
    elif (value == last):
        same += 1
    else:
        increased += 1
    last = value

print("Puzzle 2:")   
print("Increased: ")
print(increased)

print("Same: ")
print(same)

print("Decreased: ")
print(decreased)

print("")
print("")