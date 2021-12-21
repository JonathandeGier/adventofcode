from getInput import get_input
from itertools import product

def get_players():
    input = get_input(2021, 21).splitlines()
    players = {}
    for line in input:
        parts = line.split(" ")
        players[int(parts[1])] = {"pos": int(parts[-1]), "score": 0}

    return players

def has_winner(players, value):
    for player in players.values():
        if player["score"] >= value:
            return True
    return False

CALCULATED = {}
def count_wins(player1, player2, score1, score2):
    if score1 >= 21:
        return (1, 0)
    if score2 >= 21:
        return (0, 1)
    if (player1, player2, score1, score2) in CALCULATED:
        return CALCULATED[(player1, player2, score1, score2)]
    result = (0,0)
    for die1 in [1,2,3]:
        for die2 in [1,2,3]:
            for die3 in [1,2,3]:
                new_pos_player1 = (player1 + die1 + die2 + die3) % 10
                new_score1 = score1 + new_pos_player1  + 1

                player2_wins, player1_wins = count_wins(player2, new_pos_player1, score2, new_score1)
                result = (result[0] + player1_wins, result[1] + player2_wins)
    CALCULATED[(player1, player2, score1, score2)] = result
    return result

def main():
    players = get_players()

    turn = 1
    die = 1
    die_rolls = 0
    while not has_winner(players, 1000):
        move = 0
        for i in range(3):
            move += die
            die += 1
            if die > 1000:
                die = 1
            die_rolls += 1

        if turn % 2 == 0:
            # Player 2
            new_pos = players[2]["pos"] + move
            while new_pos > 10:
                new_pos -= 10
            players[2]["pos"] = new_pos
            players[2]["score"] = players[2]["score"] + new_pos
        else:
            # Player 1
            new_pos = players[1]["pos"] + move
            while new_pos > 10:
                new_pos -= 10
            players[1]["pos"] = new_pos
            players[1]["score"] = players[1]["score"] + new_pos
        
        turn += 1


    print("Puzzle 1:")
    losing_score = 2000
    for player in players:
        if players[player]["score"] < losing_score:
            losing_score = players[player]["score"]

    print(losing_score * die_rolls)
    print("")

    # reset player positions
    players = get_players()

    print("Puzzle 2:")
    print(max(count_wins(players[1]["pos"] - 1, players[2]["pos"] - 1, 0, 0)))


if __name__ == "__main__":
    main()
