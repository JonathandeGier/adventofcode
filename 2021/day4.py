from getInput import get_input


input = get_input(2021, 4).splitlines()

numbers = input[0].split(",")

bingo_cards = []

temp_card = {
    "numbers": [],
    "complete": False,
    "crossed": [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ]
}

for line in input[2:]:
    if line == '':
        bingo_cards.append(temp_card)
        temp_card = {
            "numbers": [],
            "complete": False,
            "crossed": [
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
                [False, False, False, False, False],
            ]
        }
        continue

    number_row = line.split(" ")
    number_row = [a for a in number_row if a != ""]
    
    temp_card["numbers"].append(number_row)
bingo_cards.append(temp_card)

winning_card = None
winning_number = 0

last_card = None
last_number = 0

for number in numbers:
    for card in bingo_cards:
        if card["complete"]:
            continue

        # cross of the value
        for row_i, row in enumerate(card["numbers"]):
            for column_i, value in enumerate(row):
                if value == number:
                    card["crossed"][row_i][column_i] = True
    
        # check for completed row
        for row_i, row in enumerate(card["crossed"]):
            if sum(row) == 5:
                card["complete"] = True
                if winning_card is None:
                    winning_card = card
                    winning_number = number

        # check for completed column 
        for i, x in enumerate(card["crossed"][0]):
            column = [row[i] for row in card["crossed"]]
            if sum(column) == 5:
                card["complete"] = True
                if winning_card is None:
                    winning_card = card
                    winning_number = number

        # check if the last card is completed
        completed = [tmp_card["complete"] for tmp_card in bingo_cards]
        if sum(completed) == len(bingo_cards) and last_card is None:
            last_card = card
            last_number = number

print("Puzzle 1:")
sum = 0
for row_i, row in enumerate(winning_card["numbers"]):
    for column_i, value in enumerate(row):
        if not winning_card["crossed"][row_i][column_i]:
            sum += int(value)

print("Number: " + winning_number)
print("Sum: " + str(sum))
print("Score: " + str(int(winning_number) * int(sum)))
print("")

print("Puzzle 2:")
sum = 0
for row_i, row in enumerate(last_card["numbers"]):
    for column_i, value in enumerate(row):
        if not last_card["crossed"][row_i][column_i]:
            sum += int(value)

print("Number: " + last_number)
print("Sum: " + str(sum))
print("Score: " + str(int(last_number) * int(sum)))