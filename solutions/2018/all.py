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

def main():
    days = [
        Day1(), Day2(), Day3(), Day4(), Day5(),
        Day6(), Day7(), Day8(), Day9(), Day10(),
        Day11(), Day12(), Day13(), Day14(), Day15(),
        Day16(), Day17(), Day18(), Day19(), Day20(),
    ]

    table = Table()
    table.printRow(table.headers())

    solutions = []
    for day in days:
        solution = day.solve()
        solutions.append(solution)
        table.printRow(solution)

    print("")
    times = [solution[4] for solution in solutions]
    table.printRow(("", "", "", "Total: ", sum(times)))
    
if __name__ == "__main__":
    main()