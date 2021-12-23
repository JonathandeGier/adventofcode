from getInput import get_input
from collections import deque

def get_state_1():
    input = get_input(2021, 23).splitlines()

    upper_room = input[2]
    lower_room = input[5]

    hallway = ('', '', '', '', '', '', '')
    room_a = (upper_room[3], lower_room[3])
    room_b = (upper_room[5], lower_room[5])
    room_c = (upper_room[7], lower_room[7])
    room_d = (upper_room[9], lower_room[9])

    return (hallway, room_a, room_b, room_c, room_d)

def get_state_2():
    input = get_input(2021, 23).splitlines()

    level_0 = input[2]
    level_1 = input[3]
    level_2 = input[4]
    level_3 = input[5]

    hallway = ('', '', '', '', '', '', '')
    room_a = (level_0[3], level_1[3], level_2[3], level_3[3])
    room_b = (level_0[5], level_1[5], level_2[5], level_3[5])
    room_c = (level_0[7], level_1[7], level_2[7], level_3[7])
    room_d = (level_0[9], level_1[9], level_2[9], level_3[9])

    return (hallway, room_a, room_b, room_c, room_d)

def cost(move, state):
    
    pass

def possible_moves(state):
    # move = (('x', i), ('y', j), cost) where is from location, i is from index, y is destination location, j is destination index
    moves = []

    # Moves from hallway to room
    for i, pod in enumerate(state[0]):
        if pod == "":
            continue
        elif pod == "A":
            y = 1
            if room_contains_correct_chars(state, y):
                can_go_to_room = True
                j = next_free_index_in_room(state, y)
                room_steps = j + 1
            else:
                can_go_to_room = False

            if i == 0:
                hallway_clear = state[0][1] == ""
                hallway_steps = 2
            elif i == 1 or i == 2:
                hallway_clear = True
                hallway_steps = 1
            elif i == 3:
                hallway_clear = state[0][2] == ""
                hallway_steps = 3
            elif i == 4:
                hallway_clear = state[0][2] == "" and state[0][3] == ""
                hallway_steps = 5
            elif i == 5:
                hallway_clear = state[0][2] == "" and state[0][3] == "" and state[0][4] == ""
                hallway_steps = 7
            elif i == 6:
                hallway_clear = state[0][2] == "" and state[0][3] == "" and state[0][4] == "" and state[0][5] == ""
                hallway_steps = 8

            if can_go_to_room and hallway_clear:
                moves.append(((0, i), (y, j), (room_steps + hallway_steps) * 1))
            
        elif pod == "B":
            y = 2
            if room_contains_correct_chars(state, y):
                can_go_to_room = True
                j = next_free_index_in_room(state, y)
                room_steps = j + 1
            else:
                can_go_to_room = False

            if i == 0:
                hallway_clear = state[0][1] == "" and state[0][2] == ""
                hallway_steps = 4
            elif i == 1:
                hallway_clear = state[0][2] == ""
                hallway_steps = 3
            elif i == 2 or i == 3:
                hallway_clear = True
                hallway_steps = 1
            elif i == 4:
                hallway_clear = state[0][3] == ""
                hallway_steps = 3
            elif i == 5:
                hallway_clear = state[0][3] == "" and state[0][4] == ""
                hallway_steps = 5
            elif i == 6:
                hallway_clear = state[0][3] == "" and state[0][4] == "" and state[0][5] == ""
                hallway_steps = 6

            if can_go_to_room and hallway_clear:
                moves.append(((0, i), (y, j), (room_steps + hallway_steps) * 10))
        elif pod == "C":
            y = 3
            if room_contains_correct_chars(state, y):
                can_go_to_room = True
                j = next_free_index_in_room(state, y)
                room_steps = j + 1
            else:
                can_go_to_room = False

            if i == 0:
                hallway_clear = state[0][1] == "" and state[0][2] == "" and state[0][3] == ""
                hallway_steps = 6
            elif i == 1:
                hallway_clear = state[0][2] == "" and state[0][3] == ""
                hallway_steps = 5
            elif i == 2:
                hallway_clear = state[0][3] == ""
                hallway_steps = 3
            elif i == 3 or i == 4:
                hallway_clear = True
                hallway_steps = 1
            elif i == 5:
                hallway_clear = state[0][4] == ""
                hallway_steps = 3
            elif i == 6:
                hallway_clear = state[0][4] == "" and state[0][5] == ""
                hallway_steps = 4

            if can_go_to_room and hallway_clear:
                moves.append(((0, i), (y, j), (room_steps + hallway_steps) * 100))
        elif pod == "D":
            y = 4
            if room_contains_correct_chars(state, y):
                can_go_to_room = True
                j = next_free_index_in_room(state, y)
                room_steps = j + 1
            else:
                can_go_to_room = False

            if i == 0:
                hallway_clear = state[0][1] == "" and state[0][2] == "" and state[0][3] == "" and state[0][4] == ""
                hallway_steps = 8
            elif i == 1:
                hallway_clear = state[0][2] == "" and state[0][3] == "" and state[0][4] == ""
                hallway_steps = 7
            elif i == 2:
                hallway_clear = state[0][3] == "" and state[0][4] == ""
                hallway_steps = 5
            elif i == 3:
                hallway_clear = state[0][4] == ""
                hallway_steps = 3
            elif i == 4 or i == 5:
                hallway_clear = True
                hallway_steps = 1
            elif i == 6:
                hallway_clear = state[0][5] == ""
                hallway_steps = 2

            if can_go_to_room and hallway_clear:
                moves.append(((0, i), (y, j), (room_steps + hallway_steps) * 1000))
        else:
            assert False, "Found unknown Pod"

    # Moves from room to hallway/room
    for room_i, room in enumerate(state[1:]):
        for i, val in enumerate(room):
            if val == "":
                continue

            if room_contains_correct_chars(state, room_i + 1):
                continue

            # Moves from room to Hallway to the left
            room_place = room_i + 2
            for hallway_i in range(room_place - 1, -1, -1):
                if state[0][hallway_i] != "":
                    break

                room_steps = i + 1
                hallway_steps = calculate_hallway_steps(room_place, hallway_i)
                steps = room_steps + hallway_steps
                
                if val == "B":
                    steps *= 10
                elif val == "C":
                    steps *= 100
                elif val == "D":
                    steps *= 1000

                moves.append(((room_i + 1, i), (0, hallway_i), steps))

            # Moves from room to Hallway to the right
            for hallway_i in range(room_place, 7):
                if state[0][hallway_i] != "":
                    break

                room_steps = i + 1
                hallway_steps = calculate_hallway_steps(room_place, hallway_i)
                steps = room_steps + hallway_steps
                
                if val == "B":
                    steps *= 10
                elif val == "C":
                    steps *= 100
                elif val == "D":
                    steps *= 1000

                moves.append(((room_i + 1, i), (0, hallway_i), steps))

            if val == "A" and room_contains_correct_chars(state, 1):
                if room_i == 1:
                    hallway_clear = state[0][2] == ""
                    hallway_steps = 2
                elif room_i == 2:
                    hallway_clear = state[0][2] == "" and state[0][3] == ""
                    hallway_steps = 4
                elif room_i == 3:
                    hallway_clear = state[0][2] == "" and state[0][3] == "" and state[0][4] == ""
                    hallway_steps = 6

                if hallway_clear:
                    new_room_pos = next_free_index_in_room(state, 1)

                    steps_to_hallway = i + 1
                    steps_to_room = new_room_pos + 1
                    steps = steps_to_hallway + hallway_steps + steps_to_room

                    moves.append(((room_i + 1, i), (1, new_room_pos), steps * 1))
                    
            elif val == "B" and room_contains_correct_chars(state, 2):
                if room_i == 0:
                    hallway_clear = state[0][2] == ""
                    hallway_steps = 2
                elif room_i == 2:
                    hallway_clear = state[0][3] == ""
                    hallway_steps = 2
                elif room_i == 3:
                    hallway_clear = state[0][3] == "" and state[0][4] == ""
                    hallway_steps = 4

                if hallway_clear:
                    new_room_pos = next_free_index_in_room(state, 2)

                    steps_to_hallway = i + 1
                    steps_to_room = new_room_pos + 1
                    steps = steps_to_hallway + hallway_steps + steps_to_room

                    moves.append(((room_i + 1, i), (2, new_room_pos), steps * 10))
            elif val == "C" and room_contains_correct_chars(state, 3):
                if room_i == 0:
                    hallway_clear = state[0][2] == "" and state[0][3] == ""
                    hallway_steps = 4
                elif room_i == 1:
                    hallway_clear = state[0][3] == ""
                    hallway_steps = 2
                elif room_i == 3:
                    hallway_clear = state[0][4] == ""
                    hallway_steps = 2

                if hallway_clear:
                    new_room_pos = next_free_index_in_room(state, 3)

                    steps_to_hallway = i + 1
                    steps_to_room = new_room_pos + 1
                    steps = steps_to_hallway + hallway_steps + steps_to_room

                    moves.append(((room_i + 1, i), (3, new_room_pos), steps * 100))
            elif val == "D" and room_contains_correct_chars(state, 4):
                if room_i == 0:
                    hallway_clear = state[0][2] == "" and state[0][3] == "" and state[0][4] == ""
                    hallway_steps = 6
                elif room_i == 1:
                    hallway_clear = state[0][3] == "" and state[0][4] == ""
                    hallway_steps = 4
                elif room_i == 2:
                    hallway_clear = state[0][4] == ""
                    hallway_steps = 2

                if hallway_clear:
                    new_room_pos = next_free_index_in_room(state, 4)

                    steps_to_hallway = i + 1
                    steps_to_room = new_room_pos + 1
                    steps = steps_to_hallway + hallway_steps + steps_to_room

                    moves.append(((room_i + 1, i), (4, new_room_pos), steps * 1000))

            break

    return moves

def next_free_index_in_room(state, room):
    room = state[room]
    for i in range(len(room) - 1, -1, -1):
        if room[i] == "":
            return i

def room_contains_correct_chars(state, room):
    if room == 1:
        room_val = "A"
    if room == 2:
        room_val = "B"
    if room == 3:
        room_val = "C"
    if room == 4:
        room_val = "D"

    poss = "ABCD"
    poss = poss.replace(room_val, "")
    room_str = "".join(state[room])

    result = True
    for pos in poss:
        if pos in room_str:
            result = False
    return result


def calculate_hallway_steps(from_, to_):
    # from_ is the in between index, to_ is an actual index
    if from_ > to_:
        steps = ((from_ - to_) * 2) - 1
        if to_ == 0:
            steps -= 1
    else:
        from_ -= 1
        steps = ((to_ - from_) * 2) - 1
        if to_ == 6:
            steps -= 1
    return steps

def change_state(state, move):
    temp_state = [list(state[0]), list(state[1]), list(state[2]), list(state[3]), list(state[4])]

    temp_state[move[1][0]][move[1][1]] = temp_state[move[0][0]][move[0][1]]
    temp_state[move[0][0]][move[0][1]] = ""

    return (tuple(temp_state[0]), tuple(temp_state[1]), tuple(temp_state[2]), tuple(temp_state[3]), tuple(temp_state[4]))

def is_solved(state):
    for i, room in enumerate(state[1:]):
        if i == 0:
            val = "A"
        elif i == 1:
            val = "B"
        elif i == 2:
            val = "C"
        elif i == 3:
            val = "D"

        for char in room:
            if char != val:
                return False
    return True


def main():
    state = get_state_1()
    
    all_costs = []
    state_costs = {}
    start = (state, [], 0)
    queue = deque([start])
    while queue:
        state, moves, cost = queue.popleft()

        if is_solved(state):
            all_costs.append(cost)

        if state not in state_costs or state_costs[state] > cost:
            state_costs[state] = cost

            for move in possible_moves(state):
                new_state = change_state(state, move)
                new_moves = moves.copy()
                new_moves.append(move)
                new_cost = cost + move[2]

                queue.append((new_state, new_moves, new_cost))


    print("Puzzle 1:")
    print(min(all_costs))
    print("")

    state = get_state_2()

    all_costs = []
    state_costs = {}
    start = (state, [], 0)
    queue = deque([start])
    while queue:
        state, moves, cost = queue.popleft()

        if is_solved(state):
            all_costs.append(cost)

        if state not in state_costs or state_costs[state] > cost:
            state_costs[state] = cost

            for move in possible_moves(state):
                new_state = change_state(state, move)
                new_moves = moves.copy()
                new_moves.append(move)
                new_cost = cost + move[2]

                queue.append((new_state, new_moves, new_cost))

    print("Puzzle 2:")
    print(min(all_costs))


if __name__ == "__main__":
    main()
