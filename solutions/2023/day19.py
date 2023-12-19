from Table import Table
from time import time

WORKFLOWS = {}

class Workflow:
    def __init__(self, id: str, rules: str):
        self.id = id
        self.rules = []

        for rule in rules.split(','):
            if ':' in rule:
                condition, result = rule.split(':')
                key = condition[0]
                operator = condition[1]
                value = int(condition[2:])
                self.rules.append((key, operator, value, result))
            else:
                self.rules.append((rule))
        print(self.rules)


    def accepted(self, item: dict) -> bool:
        pass

    def __passes(self, rule: tuple, item: dict) -> bool:
        pass

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Aplenty"
        self.input = self.getInput(self.day)

    def parse_workflows(self):
        WORKFLOWS = {}
        for line in self.input.split('\n\n')[0].splitlines():
            id, rules = line.split('{')
            WORKFLOWS[id] = Workflow(id, rules[:-1])

    def solve(self):
        start_time = time()

        self.parse_workflows()

        part1 = "None"
        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
