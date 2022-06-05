from functools import reduce
from Table import Table
from time import time

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Knot Hash"
        self.input = self.getInput(self.day).strip()

    def get_lengths(self):
        return [int(val) for val in self.input.split(',')]

    def hash(self, string: str) -> str:
        input_lengths = [ord(char) for char in string]
        input_lengths += [17, 31, 73, 47, 23]

        array = list(range(256))
        current_position = 0
        skip_size = 0

        for _ in range(64):
            array, current_position, skip_size = self.round(array, current_position, skip_size, input_lengths)

        dence_hash = []
        for i in range(0, 256, 16):
            dence_hash.append(reduce(lambda a, b: a ^ b, array[i:i + 16]))

        hex_hash = []
        for val in dence_hash:
            hex_val = hex(val)[2:]
            if len(hex_val) == 1:
                hex_val = '0' + hex_val
            hex_hash.append(hex_val)

        return ''.join(hex_hash)

    def round(self, array: list, current_position: int, skip_size: int, lengths: list) -> tuple:
        for length in lengths:
            selected_sequence = []
            for i in range(length):
                selected_sequence.append(array[(current_position + i) % len(array)])

            selected_sequence = selected_sequence[::-1]

            for i in range(length):
                array[(current_position + i) % len(array)] = selected_sequence[i]

            current_position = (current_position + length + skip_size) % len(array)

            skip_size += 1

        return array, current_position, skip_size

    def solve(self):
        start_time = time()

        array, _, _ = self.round(list(range(256)), 0, 0, self.get_lengths())
        
        part1 = array[0] * array[1]
        part2 = self.hash(self.input)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
