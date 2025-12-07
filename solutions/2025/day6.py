from Table import Table
from time import time

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Trash Compactor"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        operatorLine = None
        for line in self.input.splitlines():
            if '+' in line or '*' in line:
                operatorLine = line

        problems = []
        for line in self.input.splitlines():
            if line == operatorLine:
                continue

            operatorIndex = 0
            numberIndex = 0
            while operatorIndex < len(line):
                # Add the operator to the start of the math problem
                if len(problems) <= numberIndex:
                    problems.append([operatorLine[operatorIndex]])

                # Find the length of the column based on the operator line
                numStart = operatorIndex
                size = 0
                operatorIndex += 1
                while operatorIndex < len(line) and operatorLine[operatorIndex] == ' ':
                    size += 1
                    operatorIndex += 1

                if operatorIndex == len(line):
                    size += 1

                # add the number to the problem
                number = line[numStart:numStart+size]
                problems[numberIndex].append(number)

                numberIndex += 1


        part1 = 0
        for problem in problems:
            if problem[0] == '+':
                part1 += sum([int(x) for x in problem[1:]])
            elif problem[0] == '*':
                val = 1
                for num in problem[1:]:
                    val *= int(num)
                part1 += val
            else:
                assert False, 'Unknown math problem: ' + str(problem)

        part2 = 0
        for problem in problems:
            numbers = []
            for i in range(len(problem[1])):
                numbers.append(int(''.join([num[i] for num in problem[1:]])))

            if problem[0] == '+':
                part2 += sum(numbers)
            elif problem[0] == '*':
                val = 1
                for num in numbers:
                    val *= int(num)
                part2 += val
            else: 
                assert False, 'Unknown math problem: ' + str(problem)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
