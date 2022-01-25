import json
from Table import Table
from time import time

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "JSAbacusFramework.io"
        self.input = self.getInput(self.day)

    def get_data(self):
        return json.loads(self.input)

    def deep_sum(self, item):
        if type(item) == int:
            return item
        if type(item) == str:
            return 0

        sum = 0
        if type(item) == dict:
            for subItem in item.values():
                sum += self.deep_sum(subItem)
        for subItem in item:
                sum += self.deep_sum(subItem)
        return sum


    def deep_sum_no_red(self, item):
        if type(item) == int:
            return item
        if type(item) == str:
            return 0

        sum = 0
        if type(item) == dict:
            for val in item.values():
                if type(val) == str and val == "red":
                    return 0

            for subItem in item.values():
                sum += self.deep_sum_no_red(subItem)
        for subItem in item:
                sum += self.deep_sum_no_red(subItem)
        return sum

    def solve(self):
        start_time = time()

        data = self.get_data()
        part1 = self.deep_sum(data)

        part2 = self.deep_sum_no_red(data)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
