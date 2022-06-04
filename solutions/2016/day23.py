from Table import Table
from time import time

class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "Safe Cracking"
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

    def print_instructions(self, instructions):
        for instruction in instructions:
            print(instruction)
        print('')

    def run(self, instructions, p2 = False):
        registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
        }

        def get_value(input) -> int:
            if input in registers:
                return registers[input]
            return input

        if not p2:
            registers['a'] = 7
        else:
            registers['a'] = 12

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

            elif instruction[0] == 'mul':
                a = get_value(instruction[1])
                b = get_value(instruction[2])

                if instruction[3] in registers:
                    registers[instruction[3]] = a * b

            elif instruction[0] == 'tgl':
                target_i = i + get_value(instruction[1])
                is_in_program = target_i >= 0 and target_i < len(instructions)

                if is_in_program:
                    target_instruction = instructions[target_i]
                    if len(target_instruction) == 2:
                        if target_instruction[0] == 'inc':
                            new_instruction = ('dec', target_instruction[1])
                        else:
                            new_instruction = ('inc', target_instruction[1])
                    elif len(target_instruction) == 3:
                        if target_instruction[0] == 'jnz':
                            new_instruction = ('cpy', target_instruction[1], target_instruction[2])
                        else:
                            new_instruction = ('jnz', target_instruction[1], target_instruction[2])
                    else:
                        assert False, "Unknown instruction length"

                    instructions[target_i] = new_instruction
            elif instruction[0] == 'nop':
                pass
            else:
                assert False, 'Unknown instruction: ' + instruction[0]

            i += 1

        return registers

    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        result = self.run(instructions)
        part1 = result['a']

        instructions = self.get_instructions()

        # Modify instructions with multiply operator
        # 2: cpy a d               mul a b a
        # 3: cpy 0 a               cpy 0 c
        # 4: cpy b c               cpy 0 d
        # 5: inc a         -->     nop
        # 6: dec c                 nop
        # 7: jnz c -2              nop
        # 8: dec d                 nop
        # 9: jnz d -5              nop
        instructions[2] = ('mul', 'a', 'b', 'a')
        instructions[3] = ('cpy', 0, 'c')
        instructions[4] = ('cpy', 0, 'd')
        instructions[5] = tuple(['nop'])
        instructions[6] = tuple(['nop'])
        instructions[7] = tuple(['nop'])
        instructions[8] = tuple(['nop'])
        instructions[9] = tuple(['nop'])

        result = self.run(instructions, True)
        part2 = result['a']

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
