from Table import Table
from time import time

class Marble:

    def __init__(self, value):
        self.value = value
        self.left = None # counter clockwise
        self.right = None # clockwise

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Marble Mania"
        self.input = self.getInput(self.day)

    def print_circle(circle, start_marble):
        mar = start_marble.right
        print(start_marble.value, end=' ')
        while True:
            if mar.value == 0:
                break

            print(mar.value, end=' ')
            mar = mar.right
        print('')

    def play(self, players, marbles):
        scores = [0 for _ in range(players)]

        current_marble = Marble(0)
        current_marble.left = current_marble
        current_marble.right = current_marble

        for value in range(1, marbles + 1):
            player = value % players

            if value % 23 == 0:
                scores[player] += value

                marble_to_remove = current_marble.left.left.left.left.left.left.left
                scores[player] += marble_to_remove.value
                
                marble_left = marble_to_remove.left
                marble_right = marble_to_remove.right
                marble_left.right = marble_right
                marble_right.left = marble_left

                current_marble = marble_right
            else:
                new_left_marble = current_marble.right
                new_right_marble = new_left_marble.right

                current_marble = Marble(value)
                current_marble.left = new_left_marble
                current_marble.right = new_right_marble

                new_left_marble.right = current_marble
                new_right_marble.left = current_marble
        return scores


    def solve(self):
        start_time = time()

        words = self.input.split(' ')
        players = int(words[0])
        marbles = int(words[6])

        scores1 = self.play(players, marbles)
        part1 = max(scores1)

        self.printRow((self.day, self.title, part1, '', ''), end="\r")

        scores2 = self.play(players, marbles * 100)
        part2 = max(scores2)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
