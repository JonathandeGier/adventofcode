from getInput import get_input

def get_rooms():
    input = get_input(2021, 23).splitlines()

    upper_room = input[2]
    lower_room = input[3]

    hallway = ('', '', '', '', '', '', '')
    room_a = (upper_room[3], lower_room[3])
    room_b = (upper_room[5], lower_room[5])
    room_c = (upper_room[7], lower_room[7])
    room_d = (upper_room[9], lower_room[9])

    return (hallway, room_a, room_b, room_c, room_d)

def cost(move, state):
    
    pass

def possible_moves(state):
    # move = (('x', i), ('y', j), cost) where is from location, i is from index, y is destination location, j is destination index
    moves = []

    for i, pod in enumerate(state[0]): # check pods in the hallway
        if pod == "":
            continue
        elif pod == "A":
            if state[1][1] == "":
                can_go_to_room = True
                room_steps = 1
                y = 1
                j = 1
            elif state[1][1] == "A" and state[1][0] == "":
                can_go_to_room = True
                room_steps = 2
                y = 1
                j = 0
            else: 
                can_go_to_room = False

            hallway_clear = True
            if i == 1 or i == 2:
                hallway_clear = True
                hallway_steps = 1
            if i < 1:
                hallway_steps = 2 - i
                for loc in range(i + 1, 1 + 1):
                    if state[0][loc] != "":
                        hallway_clear = False
                        break
            if i > 2:
                hallway_steps = i
                if i >= 4:
                    hallway_steps += 1
                if i >= 5:
                    hallway_steps += 1

                for loc in range(i - 1, 1, -1):
                    if state[0][loc] != "":
                        hallway_clear = False
                        break


            if can_go_to_room and hallway_clear:
                moves.append(((0, i), (y, j), room_steps + hallway_steps * 1))
            
        elif pod == "B":
            pass
        elif pod == "C":
            pass
        elif pod == "D":
            pass
        else:
            assert False, "Found unknown Pod"
    pass

def main():
    rooms = get_rooms()
    print(rooms)

    print("Puzzle 1:")

    print("")

    print("Puzzle 2:")


if __name__ == "__main__":
    main()
