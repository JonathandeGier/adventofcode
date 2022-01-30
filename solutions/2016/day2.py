from Table import Table
from time import time

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Bathroom Security"
        self.input = self.getInput(self.day)

        self.keypad1 = {
            (1,1): "1", (1,2): "2", (1,3): "3",
            (2,1): "4", (2,2): "5", (2,3): "6",
            (3,1): "7", (3,2): "8", (3,3): "9"
        }
        self.pos1 = (2,2) # start at value 5

        self.keypad2 = {
                                    (1,3): "1",
                        (2,2): "2", (2,3): "3", (2,4): "4",
            (3,1): "5", (3,2): "6", (3,3): "7", (3,4): "8", (3,5): "9",
                        (4,2): "A", (4,3): "B", (4,4): "C",
                                    (5,3): "D"
        }
        self.pos2 = (3,1) # start at value 5

    def get_moves(self):
        return [[move for move in line] for line in self.input.splitlines()]

    def move(self, direction):
        # move in both keypads
        if direction == "U":
            new_pos1 = (self.pos1[0] - 1, self.pos1[1])
            new_pos2 = (self.pos2[0] - 1, self.pos2[1])
        elif direction == "R":
            new_pos1 = (self.pos1[0], self.pos1[1] + 1)
            new_pos2 = (self.pos2[0], self.pos2[1] + 1)
        elif direction == "D":
            new_pos1 = (self.pos1[0] + 1, self.pos1[1])
            new_pos2 = (self.pos2[0] + 1, self.pos2[1])
        elif direction == "L":
            new_pos1 = (self.pos1[0], self.pos1[1] - 1)
            new_pos2 = (self.pos2[0], self.pos2[1] - 1)
        else:
            assert False

        if new_pos1 in self.keypad1:
            self.pos1 = new_pos1

        if new_pos2 in self.keypad2:
            self.pos2 = new_pos2

    def solve(self):
        start_time = time()

        line_moves = self.get_moves()

        code1 = []
        code2 = []
        for line in line_moves:
            for move in line:
                self.move(move)
            code1.append(self.keypad1[self.pos1])
            code2.append(self.keypad2[self.pos2])


        part1 = "".join([str(val) for val in code1])
        part2 = "".join([str(val) for val in code2])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
