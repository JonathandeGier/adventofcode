from Table import Table
from time import time

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "A Series of Tubes"
        self.input = self.getInput(self.day)

    def get_map(self):
        return [[char for char in line] for line in self.input.splitlines()]

    def follow(self, map):
        start_col = map[0].index('|')

        letters = []
        steps = 1
        position = (0, start_col)
        direction = 'down'
        while True:

            if direction == 'up':
                new_position = (position[0] - 1, position[1])
            elif direction == 'down':
                new_position = (position[0] + 1, position[1])
            elif direction == 'left':
                new_position = (position[0], position[1] - 1)
            elif direction == 'right':
                new_position = (position[0], position[1] + 1)
            else:
                assert False

            val = map[new_position[0]][new_position[1]]
            if val == '+':
                # Find new direction
                directions = {
                    (new_position[0] - 1, new_position[1]): 'up', 
                    (new_position[0] + 1, new_position[1]): 'down', 
                    (new_position[0], new_position[1] - 1): 'left', 
                    (new_position[0], new_position[1] + 1): 'right',
                }

                directions.pop(position)
                for new_direction in directions:
                    if map[new_direction[0]][new_direction[1]] != ' ':
                        direction = directions[new_direction]
                        break

            if val not in ['|', '-', '+']:
                letters.append(val)

            if val == ' ':
                break

            position = new_position
            steps += 1

        return letters, steps

    def solve(self):
        start_time = time()

        map = self.get_map()

        letters, steps = self.follow(map)
        part1 = ''.join(letters)
        part2 = steps

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
