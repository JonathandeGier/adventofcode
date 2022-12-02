from Table import Table
from time import time

ROCK = 'A'
PAPER = 'B'
SCISSORS = 'C'

WIN = 'Z'
TIE = 'Y'
LOSE = 'X'

MY_MOVE = {
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS,
}

# opponents move , my move
GAME_OUTCOME = {
    ROCK: {
        ROCK: TIE,
        PAPER: WIN,
        SCISSORS: LOSE,
    },
    PAPER: {
        ROCK: LOSE,
        PAPER: TIE,
        SCISSORS: WIN,
    },
    SCISSORS: {
        ROCK: WIN,
        PAPER: LOSE,
        SCISSORS: TIE,
    },
}

MOVE = {
    ROCK: {
        WIN: PAPER,
        TIE: ROCK,
        LOSE: SCISSORS,
    },
    PAPER: {
        WIN: SCISSORS,
        TIE: PAPER,
        LOSE: ROCK,
    },
    SCISSORS: {
        WIN: ROCK,
        TIE: SCISSORS,
        LOSE: PAPER,
    },
}

MOVE_SCORE = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

class Day2(Table):

    def __init__(self):
        self.day = 2
        self.title = "Rock Paper Scissors"
        self.input = self.getInput(self.day)

    def get_moves(self):
        moves = []
        for line in self.input.splitlines():
            moves.append(tuple(line.split(' ')))
        return moves

    def solve(self):
        start_time = time()

        moves = self.get_moves()
        
        part1 = 0
        for move in moves:
            score = 0
            my_move = MY_MOVE[move[1]]
            outcome = GAME_OUTCOME[move[0]][my_move]

            score += MOVE_SCORE[my_move]

            if outcome == WIN:
                score += 6
            elif outcome == TIE:
                score += 3

            part1 += score

        part2 = 0
        for move in moves:
            score = 0
            my_move = MOVE[move[0]][move[1]]

            score += MOVE_SCORE[my_move]

            if move[1] == WIN:
                score += 6
            elif move[1] == TIE:
                score += 3

            part2 += score


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day2()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
