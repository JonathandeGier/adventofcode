from Table import Table
from time import time

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Clock Signal"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(' ')
            instructions.append(tuple([self.try_to_int(val) for val in segments]))
        
        return instructions

    def try_to_int(self, val):
        try:
            return int(val)
        except:
            return val

    def run(self, instructions, a):
        registers = {
            'a': a,
            'b': 0,
            'c': 0,
            'd': 0,
        }

        output = []

        def get_value(input) -> int:
            if input in registers:
                return registers[input]
            return input

        i = 0
        while i < len(instructions):
            instruction = instructions[i]

            if instruction[0] == 'cpy':
                value = get_value(instruction[1])
                if instruction[2] in registers:
                    registers[instruction[2]] = value
            
            elif instruction[0] == 'inc':
                if instruction[1] in registers:
                    registers[instruction[1]] += 1
            
            elif instruction[0] == 'dec':
                if instruction[1] in registers:
                    registers[instruction[1]] -= 1
            
            elif instruction[0] == 'jnz':
                value = get_value(instruction[1])
                if value != 0:
                    i += (get_value(instruction[2]) - 1)

            elif instruction[0] == 'out':
                value = get_value(instruction[1])
                if value not in [0, 1]:
                    return False
                
                if len(output) > 0 and value == output[-1]:
                    return False
                output.append(value)

            else:
                assert False, 'Unknown instruction: ' + instruction[0]

            i += 1

            if len(output) > 100:
                return True
        assert False

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        a = 0
        while not self.run(instructions, a):
            a += 1

        part1 = a
        part2 = "Transmit!"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
