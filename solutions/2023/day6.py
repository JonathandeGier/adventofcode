from Table import Table
from time import time

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


    def solve(self):
        start_time = time()

        races = self.parse_races()
        
        part1 = 1
        for race in races:
            wins = 0
            for speed in range(race[0] + 1):
                time_left = race[0] - speed
                distance = speed * time_left
                if distance >= race[1]:
                    wins += 1
            part1 = part1 * wins


        _time = ''
        _distance = ''
        for race in races:
            _time += str(race[0])
            _distance += str(race[1])

        _time = int(_time)
        _distance = int(_distance)

        min_win = None
        max_win = None
        for speed in range(_time + 1):
            # moving this to a function has a significant performance impact (~1s)
            time_left = _time - speed
            distance = speed * time_left
            if distance >= _distance:
                min_win = speed
                break

        for speed in range(_time + 1, 0, -1):
            time_left = _time - speed
            distance = speed * time_left
            if distance >= _distance:
                max_win = speed
                break

        part2 = max_win - min_win + 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day6()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
