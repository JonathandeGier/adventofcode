from Table import Table
from time import time

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Red-Nosed Reports"
        self.input = self.getInput(self.day)

    def parse_reports(self):
        reports = []
        for line in self.input.splitlines():
            reports.append([int(val) for val in line.split(' ')])
        return reports


    def is_safe(self, report) -> bool:
        increasing = sorted(report)
        decreasing = sorted(report, reverse=True)

        if report != increasing and report != decreasing:
            return False
        
        for i in range(len(report) - 1):
            diff = abs(report[i] - report[i + 1])
            if diff < 1 or diff > 3:
                return False
        
        return True


    def is_safe_tolerant(self, report) -> bool:
        if self.is_safe(report):
            return True
        
        for i in range(len(report)):
            new_report = report.copy()
            del new_report[i]

            if self.is_safe(new_report):
                return True


    def solve(self):
        start_time = time()

        reports = self.parse_reports()

        part1 = sum([1 for report in reports if self.is_safe(report)])
        part2 = sum([1 for report in reports if self.is_safe_tolerant(report)])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
