from typing import Counter
from Table import Table
from time import time

class Room:
    def __init__(self, raw: str):
        split = raw.split('[')
        split_2 = split[0].split('-')

        self.names = split_2[:-1]
        self.sector = int(split_2[-1])
        self.checksum = split[1].split(']')[0]

        self.name = None
        self.shift = 1

    def is_real(self):
        count = Counter("".join(self.names))
        common = count.most_common()
        common.sort(key=lambda x: (x[1], 100 - ord(x[0])), reverse=True)

        for i in range(len(self.checksum)):
            if self.checksum[i] != common[i][0]:
                return False

        return True

    def decrypt(self):
        name = "".join(self.names)
        
        decoded = []
        for char in name:
            code = ord(char)
            code += self.shift
            if code > 122:
                code -= 26

            decoded.append(chr(code))

        decoded_name = "".join(decoded)
        self.name = decoded_name
        self.shift += 1

        return decoded_name


class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Security Through Obscurity"
        self.input = self.getInput(self.day)

    def get_rooms(self):
        return [Room(line) for line in self.input.splitlines()]

    def solve(self):
        start_time = time()

        rooms = self.get_rooms()
        real_rooms = [room for room in rooms if room.is_real()]

        part1 = sum([room.sector for room in real_rooms])

        part2 = "- Not Found -"
        for room in real_rooms:
            do_break = False

            for _ in range(26):
                name = room.decrypt()

                if "northpole" in name:
                    part2 = str(room.sector)
                    do_break = True
                    break

            if do_break:
                break

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
