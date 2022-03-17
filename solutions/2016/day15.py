from Table import Table
from time import time

class Disc:
    def __init__(self, id: int, positions: int, current: int):
        self.id = id
        self.positions = positions
        self.current = current

    def step(self, steps: int = 1):
        self.current += steps

        while self.current >= self.positions:
            self.current -= self.positions

        while self.current < 0:
            self.current += self.positions

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Timing is Everything"
        self.input = self.getInput(self.day)

    def get_discs(self):
        discs = []
        for line in self.input.splitlines():
            segments = line.split(" ")
            id = int(segments[1][1])
            positions = int(segments[3])
            current = int(segments[-1][:-1])
            discs.append(Disc(id, positions, current))

        return discs

    def timer(self, discs: list):
        i = 0
        while True:
            is_aligned = True
            for disc in discs:
                if disc.current != 0:
                    is_aligned = False

            if is_aligned:
                break

            i += 1

            for disc in discs:
                disc.step()

        return i

    def solve(self):
        start_time = time()

        discs = self.get_discs()
        
        # align discs
        for disc in discs:
            disc.step(disc.id)

        part1 = str(self.timer(discs))


        # Part 2: reload discs with extra
        discs = self.get_discs()
        discs.append(Disc(7, 11, 0))
        
        # align discs
        for disc in discs:
            disc.step(disc.id)

        part2 = str(self.timer(discs))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
