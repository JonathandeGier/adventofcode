from Table import Table
from time import time

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Aunt Sue"
        self.input = self.getInput(self.day)

    def getSues(self):
        sues = {}
        for sue in self.input.splitlines():
            parts = sue.split(":")
            sueId = parts[0].split(" ")[1]

            elements = "".join(parts[1:]).split(",")
            elements = [element.strip() for element in elements]

            properties = {}
            for elem in elements:
                key, value = elem.split(" ")
                value = int(value)
                properties[key] = value

            sues[sueId] = properties
        return sues

    def matches_1(self, sueProps, data):
        for key in data:
            if key in sueProps:
                if sueProps[key] != data[key]:
                    return False
        return True

    def matches_2(self, sueProps, data):
        for key in data:
            if key in sueProps:
                if key in ["cats", "trees"] and sueProps[key] <= data[key]:
                    return False

                if key in ["pomeranians", "goldfish"] and sueProps[key] >= data[key]:
                    return False

                if key not in ["cats", "trees", "pomeranians", "goldfish"] and sueProps[key] != data[key]:
                    return False
        return True

    def solve(self):
        start_time = time()

        data = {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1
        }

        sues = self.getSues()
        
        for sue in sues:
            if self.matches_1(sues[sue], data):
                part1 = sue
                break

        for sue in sues:
            if self.matches_2(sues[sue], data):
                part2 = sue
                break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
