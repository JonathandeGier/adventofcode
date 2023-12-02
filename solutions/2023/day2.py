from Table import Table
from time import time

RED = 'red'
GREEN = 'green'
BLUE = 'blue'

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Cube Conundrum"
        self.input = self.getInput(self.day)

    def parse_games(self):
        games = {}
        for line in self.input.splitlines():
            game, sets = line.split(': ')
            game_id = int(game.split(' ')[1])
            games[game_id] = []

            for set_values in sets.split('; '):
                games[game_id].append(self.parse_set(set_values))

        return games

    def parse_set(self, set_values: str) -> tuple:
        values = [0, 0, 0] # RGB
        for value in set_values.split(', '):
            num, color = value.split(' ')
            if color == RED:
                values[0] = int(num)
            elif color == GREEN:
                values[1] = int(num)
            elif color == BLUE:
                values[2] = int(num)
        return tuple(values)
    
    def possible(self, game: list, red: int, green: int, blue: int) -> bool:
        for set_values in game:
            if set_values[0] > red or set_values[1] > green or set_values[2] > blue:
                return False
        return True
    
    def min_power(self, game: list) -> int:
        red = 0
        green = 0
        blue = 0
        for set_values in game:
            red = max(red, set_values[0])
            green = max(green, set_values[1])
            blue = max(blue, set_values[2])

        return red * green * blue

    def solve(self):
        start_time = time()

        games = self.parse_games()

        part1 = sum([id for id, game in games.items() if self.possible(game, 12, 13, 14)])
        part2 = sum([self.min_power(game) for game in games.values()])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
