from Table import Table
from time import time

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Some Assembly Required"
        self.input = self.getInput(self.day)
        self.connections = {}
        self.calcutated = {}

    def get_connections(self):
        lines = self.input.splitlines()
        self.connections = {}

        for instruction in lines:
            inout = instruction.split(" -> ")
            input = inout[0].split(" ")
            output = inout[1]

            if len(input) == 3:
                self.connections[output] = {
                    "a": self.try_to_int(input[0]),
                    "b": self.try_to_int(input[2]),
                    "gate": input[1]
                }
            if len(input) == 2:
                self.connections[output] = {
                    "a": self.try_to_int(input[1]),
                    "b": '',
                    "gate": input[0]
                }
                
            if len(input) == 1:
                self.connections[output] = {
                    "a": self.try_to_int(input[0]),
                    "b": '',
                    "gate": ''
                }
        return self.connections

    def try_to_int(self, value):
        try:
            return int(value)
        except Exception:
            return value

    def get_output(self, wire):
        if isinstance(wire, int):
            return wire

        if wire in self.calcutated:
            return self.calcutated[wire]

        connection = self.connections[wire]

        if connection["gate"] == "AND":
            result = self.get_output(connection["a"]) & self.get_output(connection["b"])
            self.calcutated[wire] = result
            return result
        elif connection["gate"] == "OR":
            result = self.get_output(connection["a"]) | self.get_output(connection["b"])
            self.calcutated[wire] = result
            return result
        elif connection["gate"] == "NOT":
            result = ~ self.get_output(connection["a"])
            self.calcutated[wire] = result
            return result
        elif connection["gate"] == "LSHIFT":
            result = self.get_output(connection["a"]) << self.get_output(connection["b"])
            self.calcutated[wire] = result
            return result
        elif connection["gate"] == "RSHIFT":
            result = self.get_output(connection["a"]) >> self.get_output(connection["b"])
            self.calcutated[wire] = result
            return result
        else: # no gate
            if isinstance(connection["a"], int):
                self.calcutated[wire] = connection["a"]
                return connection["a"]
            else:
                return self.get_output(connection["a"])


    def solve(self):
        start_time = time()

        self.get_connections()
        part1 = self.get_output("a")

        self.connections["b"]["a"] = part1
        self.calcutated = {}

        part2 = self.get_output("a")

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
