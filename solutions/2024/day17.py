from Table import Table
from time import time
import heapq

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Chronospatial Computer"
        self.input = self.getInput(self.day)

    def run(self, registers, program):
        ip = 0
        output = []
        while True:
            try:
                optcode = program[ip]
                operand = program[ip+1]
            except:
                break

            def combo_value():
                if operand <= 3:
                    return operand
                elif operand == 4:
                    return registers['A']
                elif operand == 5:
                    return registers['B']
                elif operand == 6:
                    return registers['C']
                else:
                    assert False

            if optcode == 0:
                # A-division
                registers['A'] = registers['A'] // (2 ** combo_value())
            elif optcode == 1:
                # bitwise XOR
                registers['B'] = registers['B'] ^ operand
            elif optcode == 2:
                # Mod 8
                registers['B'] = combo_value() % 8
            elif optcode == 3:
                # Jump not Zero
                if registers['A'] != 0:
                    ip = operand
                    continue
            elif optcode == 4:
                # bitwise XOR
                registers['B'] = registers['B'] ^ registers['C']
            elif optcode == 5:
                # Output
                output.append(combo_value() % 8)
            elif optcode == 6:
                # B-division
                registers['B'] = registers['A'] // (2 ** combo_value())
            elif optcode == 7:
                # C-division
                registers['C'] = registers['A'] // (2 ** combo_value())

            ip += 2

        return output
    
    def correct_digits(self, sequence, program):
        correct = 0
        for i in range(len(sequence)):
            index = -1 - i
            if sequence[index] == program[index]:
                correct += 1
            else:
                break

        return correct

    def solve(self):
        start_time = time()

        reg, program = self.input.split('\n\n')
        registers = {}
        for line in reg.splitlines():
            name, val = line.split(': ')
            registers[name[-1]] = int(val)

        program = [int(code) for code in program.split(': ')[1].split(',')]

        output = self.run(registers, program)

        part1 = ','.join([str(x) for x in output])            
        part2 = 1

        queue = []
        heapq.heappush(queue, (len(program), 1))
        while len(queue) > 0:
            missing_length, value = heapq.heappop(queue)

            found = False
            for diff in range(-16, 17):
                new_value = value + diff
                if new_value < 0:
                    continue

                new_sequence = self.run({'A': new_value, 'B': 0, 'C': 0}, program)
                correct_length = self.correct_digits(new_sequence, program)
                
                if correct_length == len(program):
                    part2 = new_value
                    found = True
                    assert tuple(program) == tuple(new_sequence)
                    break

                if len(new_sequence) == correct_length:
                    heapq.heappush(queue, (len(program) - correct_length, new_value * 8))
            
            if found:
                break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
