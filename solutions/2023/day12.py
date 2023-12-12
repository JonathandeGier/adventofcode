from Table import Table
from time import time

CACHE = {}

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Hot Springs"
        self.input = self.getInput(self.day)

    def parse_lines(self):
        records = []
        for line in self.input.splitlines():
            data, sequence = line.split(' ')
            records.append((data, tuple([int(x) for x in sequence.split(',')])))
        return records


    def possibilities(self, data: str, sequence: tuple, data_pos: int, sequence_pos: int, sequence_length: int) -> int:
        # Check the cache if we calculated the possibilities for this situation before
        cache_key = (data_pos, sequence_pos, sequence_length)
        if cache_key in CACHE:
            return CACHE[cache_key]
        
        # we are at the end of the data string
        if data_pos == len(data):
            if sequence_pos == len(sequence) and sequence_length == 0:
                return 1 # we checked the last sequence and a current sequence is not in progress
            elif sequence_pos == len(sequence) - 1 and sequence[sequence_pos] == sequence_length:
                return 1 # we are at the end of the sequence
            else:
                return 0
        
        possibilities = 0
        for option in ('.', '#'):
            if data[data_pos] == option or data[data_pos] == '?':
                if option == '.' and sequence_length == 0:
                    # Add a dot that is not at the end of a sequence
                    possibilities += self.possibilities(data, sequence, data_pos + 1, sequence_pos, 0)
                elif option == '.' and sequence_length > 0 and sequence_pos < len(sequence) and sequence[sequence_pos] == sequence_length:
                    # Add a dot that __is__ at the end of a sequence, so we start checking the next one
                    possibilities += self.possibilities(data, sequence, data_pos + 1, sequence_pos + 1, 0)
                elif option == '#':
                    # add a # that counts to the sequence
                    possibilities += self.possibilities(data, sequence, data_pos + 1, sequence_pos, sequence_length + 1)
        CACHE[cache_key] = possibilities

        return possibilities    


    def solve(self):
        start_time = time()

        records = self.parse_lines()

        part1 = 0
        for data, sequence in records:
            CACHE.clear()
            part1 += self.possibilities(data, sequence, 0, 0, 0)   
        
        part2 = 0
        for data, sequence in records:
            data = data + ('?') + data + ('?') + data + ('?') + data + ('?') + data
            sequence *= 5

            CACHE.clear()
            part2 += self.possibilities(data, sequence, 0, 0, 0)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
