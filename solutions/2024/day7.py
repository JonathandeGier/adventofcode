from Table import Table
from time import time
from itertools import product

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Bridge Repair"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        # Parsing
        equations = []
        for line in self.input.splitlines():
            result, numbers = line.split(': ')
            equations.append((int(result), [int(x) for x in numbers.split(' ')]))

        
        part1 = 0
        part2 = 0
        for equation in equations:
            possible = False
            with_concat = False
            for operators in product(['+', '*', '||'], repeat=len(equation[1]) - 1):
                op_result = equation[1][0]
                for i in range(len(equation[1]) - 1):
                    if operators[i] == '+':
                        op_result += equation[1][i+1]
                    elif operators[i] == '*':
                        op_result *= equation[1][i+1]
                    elif operators[i] == '||':
                        op_result = int(str(op_result) + str(equation[1][i+1]))
                
                if op_result == equation[0]:
                    possible = True
                    try:
                        operators.index('||')
                        with_concat = True
                    except:
                        pass
                    break
            
            if possible:
                part2 += equation[0]
                if not with_concat:
                    part1 += equation[0]


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
