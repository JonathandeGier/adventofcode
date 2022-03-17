import hashlib
import heapq
from typing import Deque
from Table import Table
from time import time

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Two Steps Forward"
        self.input = self.getInput(self.day).strip()

    def is_open(self, letter: str):
        if letter in "bcdef":
            return True
        else:
            return False

    def get_directions(self, hash: str):
        directions = []
        if self.is_open(hash[0]):
            directions.append((-1, 0, 'U'))
        if self.is_open(hash[1]):
            directions.append((1, 0, 'D'))
        if self.is_open(hash[2]):
            directions.append((0, -1, 'L'))
        if self.is_open(hash[3]):
            directions.append((0, 1, 'R'))

        return directions

    def shortest_path(self, start: tuple, end: tuple):
        queue = []
        tie_breaker = 0

        heapq.heappush(queue, (0, tie_breaker, start, ""))
        while len(queue) > 0:
            _, _, position, path = heapq.heappop(queue)

            if position == end:
                return path

            hash_string = self.input + path
            hash = hashlib.md5(hash_string.encode()).hexdigest()

            directions = self.get_directions(hash)

            for direction in directions:
                new_pos = (position[0] + direction[0], position[1] + direction[1])

                if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > 3 or new_pos[1] > 3:
                    # out of bounds
                    continue

                new_path = path + direction[2]

                tie_breaker += 1
                length = len(new_path)

                heapq.heappush(queue, (length, tie_breaker, new_pos, new_path))

    def longest_path(self, start: tuple, end: tuple):
        queue = Deque()

        queue.append((start, ""))

        paths = []

        while len(queue) > 0:
            position, path = queue.pop()

            if position == end:
                paths.append(path)
                continue

            hash_string = self.input + path
            hash = hashlib.md5(hash_string.encode()).hexdigest()

            directions = self.get_directions(hash)

            for direction in directions:
                new_pos = (position[0] + direction[0], position[1] + direction[1])

                if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > 3 or new_pos[1] > 3:
                    # out of bounds
                    continue

                new_path = path + direction[2]

                queue.append((new_pos, new_path))

        longest_path = ""
        for path in paths:
            if len(path) > len(longest_path):
                longest_path = path

        return longest_path


    def solve(self):
        start_time = time()

        part1 = self.shortest_path((0,0), (3,3))

        part2 = len(self.longest_path((0,0), (3,3)))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
