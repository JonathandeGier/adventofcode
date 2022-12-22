from Table import Table
from time import time

class Monkey:
    def __init__(self, name: str, first_name: str, second_name: str, value: int, operation: str):
        self.name = name
        self.first_name = first_name
        self.second_name = second_name

        self.value = value
        self.operation = operation

        self.first = None
        self.second = None

    def eval(self):
        if self.value is not None:
            return self.value

        first = self.first.eval()
        second = self.second.eval()

        if self.operation == '*':
            return first * second
        elif self.operation == '/':
            return first / second
        elif self.operation == '+':
            return first + second
        elif self.operation == '-':
            return first - second
        elif self.operation == '=':
            # print(first, '==', second)
            return first == second
        else:
            assert False, self.operation

    def find_human(self) -> set:
        if self.name == 'humn':
            return set([self.name])

        if self.value is not None:
            return None

        first_path = self.first.find_human()
        second_path = self.second.find_human()

        if first_path is not None:
            first_path.add(self.name)
            return first_path
        elif second_path is not None:
            second_path.add(self.name)
            return second_path
        else:
            return None

    def solve(self, path: set, value = None):
        if self.name == 'humn':
            return value

        if self.first_name in path:
            if self.operation == '=':
                new_value = self.second.eval()
            elif self.operation == '*':
                new_value = value / self.second.eval()
            elif self.operation == '/':
                new_value = value * self.second.eval()
            elif self.operation == '+':
                new_value = value - self.second.eval()
            elif self.operation == '-':
                new_value = value + self.second.eval()
            else:
                assert False

            return self.first.solve(path, new_value)
        elif self.second_name in path:
            if self.operation == '=':
                new_value = self.first.eval()
            elif self.operation == '*':
                new_value = value / self.first.eval()
            elif self.operation == '/':
                new_value = value / self.first.eval()
            elif self.operation == '+':
                new_value = value - self.first.eval()
            elif self.operation == '-':
                new_value = self.first.eval() - value
            else:
                assert False

            return self.second.solve(path, new_value)
        assert False

    def equation(self):

        if self.name == 'humn':
            return 'x'

        if self.value is not None:
            return None

        if self.name == 'root':
            self.operation = '='
        
        from_first = self.first.equation()
        from_second = self.second.equation()

        if from_first is not None:
            return '(' + from_first + ' ' + self.operation + ' ' + str(self.second.eval()) + ')'
        elif from_second is not None:
            return '(' + str(self.first.eval()) + ' ' + self.operation + ' ' + from_second + ')'
        else:
            return None

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Monkey Math"
        self.input = self.getInput(self.day)

        self.monkeys = {}

    def load_monkeys(self):
        self.monkeys = {}
        for line in self.input.splitlines():
            words = line.split(' ')

            name = words[0][:-1]
            if len(words) == 2:
                value = int(words[1])
                self.monkeys[name] = Monkey(name, None, None, value, None)
            else:
                self.monkeys[name] = Monkey(name, words[1], words[3], None, words[2])

        for name in self.monkeys:
            monkey = self.monkeys[name]
            if monkey.first_name is not None:
                monkey.first = self.monkeys[monkey.first_name]
            if monkey.second_name is not None:
                monkey.second = self.monkeys[monkey.second_name]


    def solve(self):
        start_time = time()

        self.load_monkeys()

        part1 = int(self.monkeys['root'].eval())

        self.monkeys['root'].operation = '='
        path = self.monkeys['root'].find_human()
        
        part2 = int(self.monkeys['root'].solve(path))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
