from Table import Table
from time import time
from itertools import permutations, combinations

NUM_PAD = {
    'A': (2, 3),
    '0': (1, 3),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
}

DIR_PAD = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}

DIRS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}

CACHE = {}

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Keypad Conundrum"
        self.input = self.getInput(self.day)

    def distance(self, _from, _to, keypad):
        return abs(keypad[_from][0] - keypad[_to][0]) + abs(keypad[_from][1] - keypad[_to][1])

    def goes_over_empty(self, _from, sequence, keypad):
        # Determines if the sequence goes over and empty spot from a given _from position in a keypad
        pos = keypad[_from]
        for dir in sequence:
            new_pos = (pos[0] + DIRS[dir][0], pos[1] + DIRS[dir][1])
            if new_pos not in keypad.values():
                return True
            pos = new_pos
        return False


    def keystrokes(self, _from, _to, keypad, with_cost = True):
        # Converts the _from and _to position on a keypad to a sequence that needs to be typed into the directional keypad to press the _to button
        if _from == _to:
            return 'A'

        x_diff = keypad[_to][0] - keypad[_from][0]
        y_diff = keypad[_to][1] - keypad[_from][1]

        code = []

        if y_diff < 0:
            for _ in range(abs(y_diff)):
                code.append('^')

        if x_diff > 0:
            for _ in range(x_diff):
                code.append('>')
        

        if y_diff > 0:
            for _ in range(y_diff):
                code.append('v')

        if x_diff < 0:
            for _ in range(abs(x_diff)):
                code.append('<')
        
        if with_cost:
            # lowest cost path from A > code > A that does not go over empty space
            lowest_cost = None
            lowest_cost_code = None
            for perm in permutations(code):
                if self.goes_over_empty(_from, perm, keypad):
                    continue

                prev_key = 'A'
                sequence = ''.join(perm) + 'A'
                cost_sequence = self.convert(sequence, DIR_PAD, False)
                cost = 0
                for key in cost_sequence:
                    cost += self.distance(prev_key, key, DIR_PAD)
                    prev_key = key

                if lowest_cost == None or lowest_cost > cost:
                    lowest_cost = cost
                    lowest_cost_code = sequence

            return lowest_cost_code
        else:
            return ''.join(code) + 'A'
    
    def convert(self, code, keypad, with_cost = True):
        # Convert a complete code into a code that needs to be typed into the next directional keypad
        new_code = ''
        prev_digit = 'A'
        for dig in code:
            # prev_key = new_code[-1] if len(new_code) > 0 else 'A'
            new_code += self.keystrokes(prev_digit, dig, keypad, with_cost)
            prev_digit = dig

        return new_code
    
    def code_length(self, code, target_depth, depth = 0):
        if depth == target_depth:
            return len(code)
        
        length = 0
        prev_digit = 'A'
        for dig in code:
            if (prev_digit, dig, depth) in CACHE:
                length += CACHE[(prev_digit, dig, depth)]
            else:
                keystrokes = self.keystrokes(prev_digit, dig, NUM_PAD if depth == 0 else DIR_PAD)
                keystroke_length = self.code_length(keystrokes, target_depth, depth + 1)
                length += keystroke_length

                CACHE[(prev_digit, dig, depth)] = keystroke_length

            prev_digit = dig

        return length


    def solve(self):
        start_time = time()

        codes = self.input.splitlines()

        part1 = 0
        for code in codes:
            num = int(code[:-1])
            part1 += (self.code_length(code, 3) * num)
            
        # Reset the cache to calculate the new code at deeper depth
        global CACHE
        CACHE = {}

        part2 = 0
        for code in codes:
            num = int(code[:-1])
            part2 += (self.code_length(code, 26) * num)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
