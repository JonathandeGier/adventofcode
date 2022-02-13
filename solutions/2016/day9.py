from base64 import decode
from jsii import enum
from pytest import mark
from Table import Table
from time import time

# class FileData:
#     def __init__(self, raw: str):
#         self.raw = raw

#         self.children = []



#         if "(" not in self.raw:
#             self.length = len(raw)
#         else:


class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Explosives in Cyberspace"
        self.input = self.getInput(self.day).strip()

    def decode(self, string):
        decoded = ""
        i = 0
        while i < len(string):
            char = string[i]
            if char == "(":
                # find end of marker
                for j in range(i, len(string)):
                    if string[j] == ")":
                        break

                marker = string[i+1:j]

                # decode marker
                length = int(marker.split("x")[0])
                repeat = int(marker.split("x")[1])

                # repeat marker segment
                segment = string[j+1:j+length+1]
                for _ in range(repeat):
                    decoded += segment

                i += ((j+length+1) - i)
            else:
                decoded += char
                i += 1

        return decoded

    def decode_v2(self, string):
        total_length = 0
        i = 0
        while i < len(string):
            char = string[i]
            if char == "(":
                # find end of marker
                for j in range(i, len(string)):
                    if string[j] == ")":
                        break

                marker = string[i+1:j]

                # decode marker
                length = int(marker.split("x")[0])
                repeat = int(marker.split("x")[1])

                # calculate the length of the segment
                segment = string[j+1:j+length+1]
                if "(" not in segment:
                    total_length += (length * repeat)
                else:
                    total_length += (self.decode_v2(segment) * repeat)

                i += ((j+length+1) - i)
            else:
                total_length += 1
                i += 1

        return total_length


    def solve(self):
        start_time = time()

        decoded = self.decode(self.input)
        part1 = len(decoded)

        # while "(" in decoded:
        #     decoded = self.decode(decoded)
        
        part2 = self.decode_v2(self.input)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
