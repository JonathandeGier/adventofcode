from threading import Thread
import _thread
from time import sleep, time

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
from day11 import Day11
from day12 import Day12
from day13 import Day13
from day14 import Day14
from day15 import Day15
from day16 import Day16
from day17 import Day17
from day18 import Day18
from day19 import Day19
from day20 import Day20
from day21 import Day21
from day22 import Day22
from day23 import Day23
from day24 import Day24
from day25 import Day25


def printTable(solutions, mtTime = None):
    table = Table()
    
    string = chr(27) + "[2J"

    string += table.format(table.headers())

    for solution in solutions:
        string += table.format(solution)

    times = [solution[4] for solution in solutions]
    string += "\n"
    string += table.format(("", "", "", "Total (ST): ", sum(times)))

    if mtTime is not None:
        string += table.format(("", "", "", "Total (MT): ", mtTime))

    print(string, end="")


def mtMain():
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
    day11 = Day11()
    day12 = Day12()
    day13 = Day13()
    day14 = Day14()
    day15 = Day15()
    day16 = Day16()
    day17 = Day17()
    day18 = Day18()
    day19 = Day19()
    day20 = Day20()
    day21 = Day21()
    day22 = Day22()
    day23 = Day23()
    day24 = Day24()
    day25 = Day25()

    days = [
        day1,  day2,  day3,  day4,  day5,
        day6,  day7,  day8,  day9,  day10,
        day11, day12, day13, day14, day15,
        day16, day17, day18, day19, day20,
        day21, day22, day23, day24, day25
    ]

    emptyTable = [[day.day, day.title, "", "", 0] for day in days]

    global solvedTable
    solvedTable = []

    start_time = time()

    for day in days:
        _thread.start_new_thread(mtSolve, (day, ))

    while len(solvedTable) != len(days):
        tmpTable = solvedTable.copy()
        printTable(merge_tables(tmpTable, emptyTable))
        sleep(1)

    end_time = time()
    seconds_elapsed = end_time - start_time

    printTable(merge_tables(solvedTable, emptyTable), seconds_elapsed)

    

def mtSolve(day):
    global solvedTable
    solvedTable.append(day.solve())


def merge_tables(solved, filler):
    data = []
    for day in range(1, len(filler) + 1):
        if get_day(solved, day) is not None:
            data.append(get_day(solved, day))
        else:
            data.append(get_day(filler, day))
    return data


def get_day(array: list, day: int):
    for _day in array:
        if _day[0] == day:
            return _day
    return None


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
    day11 = Day11()
    day12 = Day12()
    day13 = Day13()
    day14 = Day14()
    day15 = Day15()
    day16 = Day16()
    day17 = Day17()
    day18 = Day18()
    day19 = Day19()
    day20 = Day20()
    day21 = Day21()
    day22 = Day22()
    day23 = Day23()
    day24 = Day24()
    day25 = Day25()

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

    solutions.append(day11.solve())
    table.printRow(solutions[-1])

    solutions.append(day12.solve())
    table.printRow(solutions[-1])

    solutions.append(day13.solve())
    table.printRow(solutions[-1])

    solutions.append(day14.solve())
    table.printRow(solutions[-1])

    solutions.append(day15.solve())
    table.printRow(solutions[-1])

    solutions.append(day16.solve())
    table.printRow(solutions[-1])

    solutions.append(day17.solve())
    table.printRow(solutions[-1])

    solutions.append(day18.solve())
    table.printRow(solutions[-1])

    solutions.append(day19.solve())
    table.printRow(solutions[-1])

    solutions.append(day20.solve())
    table.printRow(solutions[-1])

    solutions.append(day21.solve())
    table.printRow(solutions[-1])

    solutions.append(day22.solve())
    table.printRow(solutions[-1])

    solutions.append(day23.solve())
    table.printRow(solutions[-1])

    solutions.append(day24.solve())
    table.printRow(solutions[-1])

    solutions.append(day25.solve())
    table.printRow(solutions[-1])

    print("")
    times = [solution[4] for solution in solutions]
    table.printRow(("", "", "", "Total (ST): ", sum(times)))



if __name__ == "__main__":
    main()