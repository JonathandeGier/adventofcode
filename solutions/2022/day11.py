from Table import Table
from time import time
import re

class Monkey:
    def __init__(self, id: int, items: list, op_op, op_b, mod: int, monkey_true: int, monkey_false: int):
        self.id: int = id
        self.items: list[int] = items
        self.op_op: str = op_op
        self.op_b: str = op_b
        self.mod: int = mod
        self.monkey_true: int = monkey_true
        self.monkey_false: int = monkey_false

        self.inspected_items: int = 0

    def throw_items(self, monkeys: dict, common_multiple = None):
        for item in self.items:
            worry_level = self._inspect(item)

            if common_multiple is None:
                worry_level = worry_level // 3
            else:
                worry_level %= common_multiple

            if worry_level % self.mod == 0:
                monkeys[self.monkey_true].catch_item(worry_level)
            else:
                monkeys[self.monkey_false].catch_item(worry_level)
        
        self.items = []

    def catch_item(self, item):
        self.items.append(item)
        

    def _inspect(self, item):
        self.inspected_items += 1

        if self.op_b == 'old':
            b = item
        else:
            b = int(self.op_b)

        if self.op_op == '*':
            return item * b
        elif self.op_op == '+':
            return item + b
        else:
            assert False


class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = "Monkey in the Middle"
        self.input = self.getInput(self.day)

        self.monkeys = {}

    def load_monkeys(self):
        self.monkeys = {}

        for raw_monkey in self.input.split('\n\n'):
            matches = re.search("^Monkey (\d)", raw_monkey)
            id = int(matches.groups()[0])

            matches = re.search("Starting items: (.*)", raw_monkey)
            items = eval('[' + matches.groups()[0] + ']')

            matches = re.search("new = old (.) (.*)", raw_monkey)
            op_op = matches.groups()[0]
            op_b = matches.groups()[1]

            matches = re.search("divisible by (\d*)", raw_monkey)
            mod = int(matches.groups()[0])
            
            matches = re.search("true: throw to monkey (\d*)", raw_monkey)
            monkey_true = int(matches.groups()[0])

            matches = re.search("false: throw to monkey (\d*)", raw_monkey)
            monkey_false = int(matches.groups()[0])

            self.monkeys[id] = Monkey(id, items, op_op, op_b, mod, monkey_true, monkey_false)

    def solve(self):
        start_time = time()

        self.load_monkeys()

        for _ in range(20):
            for id in self.monkeys:
                self.monkeys[id].throw_items(self.monkeys)

        sorted_monkeys = sorted(self.monkeys.values(), key=lambda x: x.inspected_items, reverse=True)
        part1 = sorted_monkeys[0].inspected_items * sorted_monkeys[1].inspected_items
        
        # calculate common factor
        # if a+b is divisible by x, then (a%x)+b is also divisible by x
        # if a*b is divisible by x, then (a%x)*b is also divisible by x
        # then we simply need to find a number that is divisible by all numbers in the input, which is the product
        mods = [monkey.mod for monkey in self.monkeys.values()]
        common_multiple = 1
        for mod in mods:
            common_multiple *= mod

        # reset the monkeys
        self.load_monkeys()
        
        for _ in range(10_000):
            for id in self.monkeys:
                self.monkeys[id].throw_items(self.monkeys, common_multiple)

        sorted_monkeys = sorted(self.monkeys.values(), key=lambda x: x.inspected_items, reverse=True)
        part2 = sorted_monkeys[0].inspected_items * sorted_monkeys[1].inspected_items

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
