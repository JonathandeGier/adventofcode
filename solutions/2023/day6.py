from Table import Table
from time import time
import math

class Day6(Table):

    def __init__(self):
        self.day = 6
        self.title = "Wait For It"
        self.input = self.getInput(self.day)

    def parse_races(self):
        races = {}
        for line in self.input.splitlines():
            parts = line.split()
            values = [int(x) for x in parts[1:]]
            for i, val in enumerate(values):
                if i not in races:
                    races[i] = []
                races[i].append(val)
        
        return [tuple(race) for race in races.values()]
    
    def possible_wins(self, time, distance):
        # This puzzle can be solved with the quadratic formula
        min_wait = (time - math.sqrt(time**2 - 4 * distance)) / 2
        max_wait = (time + math.sqrt(time**2 - 4 * distance)) / 2

        # round up the min wait time, if it is an integer, we must wait an extra minisecond to actually win
        if int(min_wait) == min_wait:
            min_wait += 1
        else:
            min_wait = math.ceil(min_wait)

        # round down the max wait time, if it is an integer, we must wait one milisecond less to actually win
        if int(max_wait) == max_wait:
            max_wait -= 1
        else:
            max_wait = math.floor(max_wait)

        return max_wait - min_wait + 1


    def solve(self):
        start_time = time()

        races = self.parse_races()
        
        combined_time = ''
        combined_distance = ''
        for race in races:
            combined_time += str(race[0])
            combined_distance += str(race[1])

        combined_time = int(combined_time)
        combined_distance = int(combined_distance)

        part1 = math.prod([self.possible_wins(race[0], race[1]) for race in races])
        part2 = self.possible_wins(combined_time, combined_distance)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
