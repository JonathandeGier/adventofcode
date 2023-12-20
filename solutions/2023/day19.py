from Table import Table
from time import time
from copy import deepcopy
import re

ACCEPTED = 'A'
REJECTED = 'R'
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
                self.rules.append((rule,))


    def accepted(self, item: dict) -> bool:
        for rule in self.rules:
            result = rule[-1]
            if len(rule) > 1 and not self.__passes(rule, item):
                continue

            if result == ACCEPTED:
                return True
            elif result == REJECTED:
                return False
            elif result in WORKFLOWS:
                return WORKFLOWS[result].accepted(item)
            else:
                assert False, result


    def accepted_values(self, item_possibilities: dict):
        possibilities = []
        next_possibilities = deepcopy(item_possibilities)
        for rule in self.rules:
            result = rule[-1]
            if len(rule) != 1:
                current_possibilities, next_possibilities = self.__split_possibilities(rule, next_possibilities)
            else:
                current_possibilities = next_possibilities

            if result == ACCEPTED:
                possibilities.append(current_possibilities)
            elif result == REJECTED:
                pass
            elif result in WORKFLOWS:
                for pos in WORKFLOWS[result].accepted_values(deepcopy(current_possibilities)):
                    possibilities.append(pos)
            else:
                assert False, result

        return possibilities


    def __passes(self, rule: tuple, item: dict) -> bool:
        if rule[1] == '<':
            return item[rule[0]] < rule[2]
        elif rule[1] == '>':
            return item[rule[0]] > rule[2]
        else:
            assert False, f'Unknown operator: {rule[1]}'


    def __split_possibilities(self, rule: tuple, item_possibilities: dict) -> dict:
        this = deepcopy(item_possibilities)
        next = deepcopy(item_possibilities)
        if rule[1] == '<':
            # return item[rule[0]] < rule[2]
            this[rule[0]][1] = min(rule[2] - 1, this[rule[0]][1])
            next[rule[0]][0] = max(rule[2], next[rule[0]][0])
        elif rule[1] == '>':
            this[rule[0]][0] = max(rule[2] + 1, this[rule[0]][0])
            next[rule[0]][1] = min(rule[2], next[rule[0]][1])
        else:
            assert False, f'Unknown operator: {rule[1]}'

        return this, next



class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Aplenty"
        self.input = self.getInput(self.day)


    def parse_workflows(self):
        for line in self.input.split('\n\n')[0].splitlines():
            id, rules = line.split('{')
            WORKFLOWS[id] = Workflow(id, rules[:-1])


    def parse_items(self):
        items = []
        for line in self.input.split('\n\n')[1].splitlines():
            result = re.search('{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', line).groups()
            items.append({'x': int(result[0]), 'm': int(result[1]), 'a': int(result[2]), 's': int(result[3])})
        return items


    def solve(self):
        start_time = time()

        self.parse_workflows()
        items = self.parse_items()

        part1 = 0
        for item in items:
            if WORKFLOWS['in'].accepted(item):
                part1 += sum(item.values())
            

        accepted_values = WORKFLOWS['in'].accepted_values({key: [1, 4000] for key in 'xmas'})

        part2 = 0
        for accepted_ranges in accepted_values:
            possibilities = 1
            for _min, _max in accepted_ranges.values():
                diff = _max - _min + 1
                possibilities *= diff
            
            part2 += possibilities

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
