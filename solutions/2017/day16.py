from pytest import param
from Table import Table
from time import time

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Permutation Promenade"
        self.input = self.getInput(self.day)

    def get_moves(self):
        moves = []
        for move_string in self.input.strip().split(','):
            operator = move_string[0]
            params = move_string[1:]

            if operator == 's':
                moves.append((operator, int(params)))
            elif operator == 'x':
                params = params.split('/')
                moves.append((operator, int(params[0]), int(params[1])))
            elif operator == 'p':
                params = params.split('/')
                moves.append((operator, params[0], params[1]))
            else:
                assert False
        return moves

    def dance(self, array, moves):
        for move in moves:
            if move[0] == 's':
                new_array = []
                for i in range(len(array)):
                    index = i - move[1]
                    new_array.append(array[index])
                array = new_array
            elif move[0] == 'x':
                tmp = array[move[1]]
                array[move[1]] = array[move[2]]
                array[move[2]] = tmp
            elif move[0] == 'p':
                i_1 = array.index(move[1])
                i_2 = array.index(move[2])

                tmp = array[i_1]
                array[i_1] = array[i_2]
                array[i_2] = tmp
            else:
                assert False
        return array

    def solve(self):
        start_time = time()

        start_array = [chr(i) for i in range(97, 113)]
        moves = self.get_moves()

        array = self.dance(start_array.copy(), moves)
        part1 = ''.join(array)

        array = start_array.copy()
        seen = [array]
        for i in range(1, 1_000_000_000):
            array = self.dance(array.copy(), moves)
            if tuple(array) == tuple(start_array):
                array = seen[1_000_000_000 % i]
                break
            seen.append(array)

        part2 = ''.join(array)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
