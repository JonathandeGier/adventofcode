from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "Supply Stacks"
        self.input = self.getInput(self.day)

        self.stacks = {}

    def load_stacks(self):

        stack_lines = self.input.split('\n\n')[0].splitlines()
        
        self.stacks = {}
        stack_ids = [int(val) for val in stack_lines[-1].split(' ') if val != '']
        for id in stack_ids:
            self.stacks[id] = []


        stack_values = stack_lines[:-1]
        for i in range(len(stack_values) - 1, -1, -1):
            row_values = stack_values[i]

            for id in self.stacks:
                val_index = (id - 1) * 4 + 1
                if row_values[val_index] != ' ':
                    self.stacks[id].append(row_values[val_index])

    def get_moves(self):
        move_lines = self.input.split('\n\n')[1].splitlines()
        
        moves = []
        for line in move_lines:
            segments = line.split(' ')
            moves.append((int(segments[1]), int(segments[3]), int(segments[5])))

        return moves

    def move(self, move: tuple):
        for _ in range(move[0]):
            assert len(self.stacks[move[1]]) > 0

            crate = self.stacks[move[1]].pop()
            self.stacks[move[2]].append(crate)

    def move_stacks(self, move: tuple):
        assert len(self.stacks[move[1]]) >= move[0]

        crates = self.stacks[move[1]][len(self.stacks[move[1]]) - move[0]:]
        self.stacks[move[1]] = self.stacks[move[1]][:len(self.stacks[move[1]]) - move[0]]

        for crate in crates:
            self.stacks[move[2]].append(crate)

    def solve(self):
        start_time = time()

        self.load_stacks()

        moves = self.get_moves()
        for move in moves:
            self.move(move)

        part1 = ""
        for id in self.stacks:
            part1 = part1 + self.stacks[id][-1]

        self.load_stacks()
        for move in moves:
            self.move_stacks(move)

        part2 = ""
        for id in self.stacks:
            part2 = part2 + self.stacks[id][-1]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
