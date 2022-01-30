from os import DirEntry
from Table import Table
from time import time

class Day1(Table):

    def __init__(self):
        self.day = 1
        self.title = "No Time for a Taxicab"
        self.input = self.getInput(self.day)

        self.pos = (0,0)
        self.facing = (0,1) # pos y = north
        self.visited = set()
        self.visited.add((0,0))
        self.first_visited_twice = None

    def get_directions(self):
        return [item.strip() for item in self.input.split(",")]

    def turn(self, turn):
        if turn == "R":
            if self.facing == (0,1):
                self.facing = (1,0)
            elif self.facing == (1,0):
                self.facing = (0,-1)
            elif self.facing == (0,-1):
                self.facing = (-1,0)
            elif self.facing == (-1,0):
                self.facing = (0,1)
            else:
                assert False
        elif turn == "L":
            if self.facing == (0,1):
                self.facing = (-1,0)
            elif self.facing == (1,0):
                self.facing = (0,1)
            elif self.facing == (0,-1):
                self.facing = (1,0)
            elif self.facing == (-1,0):
                self.facing = (0,-1)
            else:
                assert False
        else:
            assert False

    def move(self, distance):
        for i in range(1, distance + 1):
            offset = (i * self.facing[0], i * self.facing[1])
            visit_pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])

            if visit_pos in self.visited and self.first_visited_twice == None:
                self.first_visited_twice = visit_pos
            else:
                self.visited.add(visit_pos)

        offset = (distance * self.facing[0], distance * self.facing[1])
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])

    def solve(self):
        start_time = time()
        directions = self.get_directions()

        for direction in directions:
            turn = direction[0]
            distance = int(direction[1:])

            self.turn(turn)
            self.move(distance)

        part1 = sum([abs(item) for item in self.pos])

        part2 = sum([abs(item) for item in self.first_visited_twice])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day1()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
