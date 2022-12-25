from Table import Table
from time import time

class SNAFU:
    table = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2,
    }

    def __init__(self, value: str = '0', decimal_value: int = None):
        if decimal_value is not None:
            self.value = decimal_value
        else:
            # validate the number
            for val in value:
                if val not in self.table:
                    assert False, 'Not a valid SNAFU number: ' + val

            # convert to decimal
            decimal_value = 0
            for i in range(len(value)):
                pof = 5 ** i
                index = -1 - i
                decimal_value += self.table[value[index]] * pof

            self.value = decimal_value

    def __add__(self, other_snafu):
        return SNAFU(decimal_value=self.value + other_snafu.value)

    def __radd__(self, int_value):
        return SNAFU(decimal_value=self.value + int_value)

    def __eq__(self, __o: object) -> bool:
        if type(__o) != SNAFU:
            return False

        if self.value == __o.value:
            return True

        return False

    def __str__(self) -> str:
        # convert to regular base 5 number
        value = self.value
        base5 = ''
        while value:
            base5 = str(value % 5) + base5
            value //= 5

        # substitue out 3 and 4 and replace with = and -
        snafu = ''
        carry = 0
        for i in range(len(base5) - 1, -1, -1):
            digit = int(base5[i]) + carry
            if digit == 5:
                carry = 1
                snafu = '0' + snafu
            elif digit == 4:
                carry = 1
                snafu = '-' + snafu
            elif digit == 3:
                carry = 1
                snafu = '=' + snafu
            else:
                carry = 0
                snafu = str(digit) + snafu

        if carry == 1:
            snafu = '1' + snafu

        return snafu

class Day25(Table):

    def __init__(self):
        self.day = 25
        self.title = "Full of Hot Air"
        self.input = self.getInput(self.day)

    def get_numbers(self):
        numbers = []
        for line in self.input.splitlines():
            numbers.append(SNAFU(line))
        return numbers

    def solve(self):
        start_time = time()

        numbers = self.get_numbers()

        part1 = str(sum(numbers))
        part2 = 'Start the Blender!'

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day25()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
