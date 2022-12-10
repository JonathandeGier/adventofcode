from day1 import Day1
from day2 import Day2
from day3 import Day3
from day4 import Day4
from day5 import Day5
from day6 import Day6
from day7 import Day7
from day8 import Day8
from day9 import Day9
from day10 import Day10
from Table import Table

def main():
    days = [
        Day1(), Day2(), Day3(), Day4(), Day5(),
        Day6(), Day7(), Day8(), Day9(), Day10(),
    ]

    table = Table()
    table.printRow(table.headers())

    solutions = []
    for day in days:
        solution = day.solve()
        solutions.append(solution)
        table.printRow(solution)

    print('')
    times = [solution[4] for solution in solutions]
    table.printRow(('', '', '', 'Total: ', sum(times)))
    print('')
    
if __name__ == '__main__':
    main()