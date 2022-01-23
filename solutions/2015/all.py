from Table import Table
from day1 import Day1
from day2 import Day2
from day3 import Day3
from day4 import Day4
from day5 import Day5

def main():
    day1 = Day1()
    day2 = Day2()
    day3 = Day3()
    day4 = Day4()
    day5 = Day5()

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

    print("")
    times = [solution[4] for solution in solutions]
    table.printRow(("", "", "", "Total: ", sum(times)))



if __name__ == "__main__":
    main()