from Table import Table
from time import time

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Dragon Checksum"
        self.input = self.getInput(self.day).strip()

    def fold(self, string: str):
        a = string
        b = string[::-1]

        chars = []
        for char in b:
            if char == '1':
                chars.append('0')
            else:
                chars.append('1')

        b = "".join(chars)

        return a + '0' + b


    def checksum(self, string: str):
        while len(string) % 2 == 0:
            pairs = []
            for i in range(0, len(string), 2):
                pairs.append(string[i:i+2])

            result = []
            for pair in pairs:
                if pair in ['00', '11']:
                    result.append('1')
                else:
                    result.append('0')

            string = "".join(result)

        return string

    
    def disk_checksum(self, length: int):

        state = self.input
        while len(state) < length:
            state = self.fold(state)

        state = state[:length]

        return self.checksum(state)


    def solve(self):
        start_time = time()

        disk_length = 272

        state = self.input
        while len(state) < disk_length:
            state = self.fold(state)

        state = state[:disk_length]

        part1 = self.disk_checksum(272)
        part2 = self.disk_checksum(35651584)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
