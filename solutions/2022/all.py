from day1 import Day1
from day2 import Day2
from day3 import Day3
from day4 import Day4
from Table import Table

def main():
    days = [
        Day1(), Day2(), Day3(), Day4(),
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