from Table import Table
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

def main():
    day1 = Day1()
    day2 = Day2()
    day3 = Day3()
    day4 = Day4()
    day5 = Day5()
    day6 = Day6()
    day7 = Day7()
    day8 = Day8()
    day9 = Day9()
    day10 = Day10()

    table = Table()
    table.printRow(table.headers())

    solutions = []

    solutions.append(day1.solve())
    table.printRow(solutions[-1])

    solutions.append(day2.solve())
    table.printRow(solutions[-1])

    solutions.append(day3.solve())
    table.printRow(solutions[-1])

    solutions.append(day4.solve())
    table.printRow(solutions[-1])

    solutions.append(day5.solve())
    table.printRow(solutions[-1])

    solutions.append(day6.solve())
    table.printRow(solutions[-1])

    solutions.append(day7.solve())
    table.printRow(solutions[-1])

    solutions.append(day8.solve())
    table.printRow(solutions[-1])

    solutions.append(day9.solve())
    table.printRow(solutions[-1])

    solutions.append(day10.solve())
    table.printRow(solutions[-1])

    print("")
    times = [solution[4] for solution in solutions]
    table.printRow(("", "", "", "Total: ", sum(times)))



if __name__ == "__main__":
    main()