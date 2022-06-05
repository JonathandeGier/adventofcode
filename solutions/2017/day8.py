from Table import Table
from time import time

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "I Heard You Like Registers"
        self.input = self.getInput(self.day)

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(' ')
            reg = segments[0]
            op = segments[1]
            val = int(segments[2])
            cond_reg = segments[4]
            cond_op = segments[5]
            cond_val = int(segments[6])

            instructions.append((reg, op, val, (cond_reg, cond_op, cond_val)))

        return instructions

    def run(self, instructions):
        registers = {}
        highest_value = 0

        def get_register_val(register):
            if register not in registers:
                registers[register] = 0

            return registers[register]

        def passes_condition(condition):
            reg_val = get_register_val(condition[0])
            val = condition[2]

            if condition[1] == '<':
                return reg_val < val
            elif condition[1] == '>':
                return reg_val > val
            elif condition[1] == '<=':
                return reg_val <= val
            elif condition[1] == '>=':
                return reg_val >= val
            elif condition[1] == '==':
                return reg_val == val
            elif condition[1] == '!=':
                return reg_val != val
            else:
                assert False, 'Unknown operator: ' + condition[1]

        for instruction in instructions:
            if not passes_condition(instruction[3]):
                continue

            # make the register if it does not exist
            get_register_val(instruction[0])

            val = instruction[2]
            if instruction[1] == 'inc':
                registers[instruction[0]] += val
            elif instruction[1] == 'dec':
                registers[instruction[0]] -= val
            else:
                assert False, 'Unknown instruction: ' + instruction[1]

            highest_value = max(highest_value, registers[instruction[0]])

        return registers, highest_value


    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        registers, highest_value = self.run(instructions)

        largest_value = 0
        for register in registers:
            largest_value = max(largest_value, registers[register])

        part1 = largest_value
        part2 = highest_value

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
