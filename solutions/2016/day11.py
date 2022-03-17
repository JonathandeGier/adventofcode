import heapq
from Table import Table
from time import time
from itertools import combinations

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Radioisotope Thermoelectric Generators"
        self.input = self.getInput(self.day)
        self.object_count = 0

    # loads the input
    def load_floors(self):
        floor = 1
        state = {}
        self.object_count = 0

        for line in self.input.splitlines():
            objects = []

            line = line.replace(',', '')
            line = line.replace('.', '')

            segments = line.split(" ")
            for i, segment in enumerate(segments):
                if segment in ["generator", "microchip"]:
                    _type = segments[i-1]
                    objects.append(_type[0].upper() + segment[0].upper())
                    self.object_count += 1

            state[floor] = objects
            floor += 1

        return state

    # determines the possible moves depending on the game state and current floor
    def possible_moves(self, state: dict, current_floor: int):
        comb_array = state[current_floor].copy()
        comb_array.append(None)

        moves = []

        for poss in combinations(comb_array, 2):
            if current_floor < 4:
                moves.append(('U', poss[0], poss[1]))
            if current_floor > 1:
                moves.append(('D', poss[0], poss[1]))

        return moves

    # apply a move to the current game state
    def apply(self, move: tuple, state: dict, current_floor: int):
        new_state = {}
        for key in state:
            new_state[key] = state[key].copy()

        if move[0] == 'U':
            new_floor = current_floor + 1
        else:
            new_floor = current_floor - 1

        new_state[current_floor].remove(move[1])
        new_state[new_floor].append(move[1])

        if move[2] is not None:
            new_state[current_floor].remove(move[2])
            new_state[new_floor].append(move[2])
        

        return new_state, new_floor

    # determines if a given state is safe i.e. wont fry a chip
    def is_safe(self, state: dict):
        for floor in state:
            contents = state[floor]

            for item in contents:
                if item[1] == 'M':
                    if item[0] + 'G' in contents:
                        continue
                    else:
                        for item2 in contents:
                            if item2[1] == 'G':
                                return False
        return True


    # determines if the current game state is the final game state
    def is_completed(self, state: dict, current_floor: int):
        return len(state[4]) == self.object_count and current_floor == 4


    # make a hashable type of the game state
    def hashable(self, state: dict, current_floor: int):
        arr = []
        for floor in range(1,5):
            contents = state[floor].copy()
            contents.sort()
            
            arr.append(floor)
            if floor == current_floor:
                arr.append('current')
            arr.append("".join(contents))
        return tuple(arr)


    # determines the priority for this game state
    # lower priority means first to add moves to
    def priority(self, state: dict, moves: int):
        result = 0
        for floor in state:
            amplifier = abs(floor - 4)
            result += len(state[floor]) * amplifier
        return result + moves


    # main function to move all generators and microchips to the top
    def move_to_top(self, state: dict):
        queue = []
        tie_breaker = 0
        calculated = {}

        solved_moves = None

        # (move_count, prio, tie_breaker, state, current_floor, moves)
        queue_item = (0, tie_breaker, state, 1, [])
        heapq.heappush(queue, queue_item)
        while len(queue) > 0:
            # get the current game state
            _, _, state, current_floor, moves = heapq.heappop(queue)

            # check if the current game state has already been calculated
            calc_key = self.hashable(state, current_floor)
            if calc_key in calculated and calculated[calc_key] < len(moves):
                continue 

            # check if the current game state is the desired state
            if self.is_completed(state, current_floor):
                solved_moves = moves
                break

            # apply each possible move
            possible_moves = self.possible_moves(state, current_floor)
            for move in possible_moves:
                local_moves = moves.copy()
                local_moves.append(move)
                new_state, new_floor = self.apply(move, state, current_floor)
                calc_key = self.hashable(new_state, new_floor)

                # only continue if the state is safe and it has not beet calculated before
                if self.is_safe(new_state) and (calc_key not in calculated or calculated[calc_key] > len(local_moves)):
                    calculated[calc_key] = len(local_moves)
                    prio = self.priority(new_state, len(local_moves))
                    tie_breaker += 1
                    heapq.heappush(queue, (prio, tie_breaker, new_state, new_floor, local_moves))

        assert solved_moves is not None, 'Unable to solve'

        return solved_moves

    def solve(self):
        start_time = time()

        state = self.load_floors()
        part1 = len(self.move_to_top(state))

        state = self.load_floors()
        state[1].append('EG')
        state[1].append('EM')
        state[1].append('DG')
        state[1].append('DM')
        self.object_count += 4

        part2 = len(self.move_to_top(state))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
