from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Perfectly Spherical Houses in a Vacuum"
        self.input = self.getInput(self.day)

    def get_lines(self):
        lines = self.input.splitlines()
        return lines

    def solve(self):
        start_time = time()

        # Part 1
        visited = {
            "0,0": 1
        }

        x = 0
        y = 0
        for char in self.input:
            if char == "^":
                y += 1
            if char == "v":
                y -= 1
            if char == "<":
                x -= 1
            if char == ">":
                x += 1

            location = str(x) + "," + str(y)
            if location not in visited:
                visited[location] = 1
            else:
                visited[location] += 1
            
        multiple_visits = 0
        for count in visited.values():
            if count >= 1:
                multiple_visits += 1
        part1 = multiple_visits


        # Part 2
        visited = {
            "0,0": 2
        }

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        for i, char in enumerate(self.input):
            if i % 2 == 0:
                if char == "^":
                    y1 += 1
                if char == "v":
                    y1 -= 1
                if char == "<":
                    x1 -= 1
                if char == ">":
                    x1 += 1

                location = str(x1) + "," + str(y1)
                if location not in visited:
                    visited[location] = 1
                else:
                    visited[location] += 1
            if i % 2 != 0:
                if char == "^":
                    y2 += 1
                if char == "v":
                    y2 -= 1
                if char == "<":
                    x2 -= 1
                if char == ">":
                    x2 += 1
                
                location = str(x2) + "," + str(y2)
                if location not in visited:
                    visited[location] = 1
                else:
                    visited[location] += 1
            
        multiple_visits = 0
        for count in visited.values():
            if count >= 1:
                multiple_visits += 1
        part2 = multiple_visits

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
