from Table import Table
from time import time
from PIL import Image

NEXT_POSITIONS = [
    ((0, -1), (1, -1), (-1, -1), (0, -1)),
    ((0, 1), (1, 1), (-1, 1), (0, 1)),
    ((-1, 0), (-1, 1), (-1, -1), (-1, 0)),
    ((1, 0), (1, -1), (1, 1), (1, 0)),
]

class Elf:
    def __init__(self, position: tuple):
        self.position = position
        self.offset = 0

    def next_position(self, other_elfs: set):
        next_position = self.position

        all_clear = True
        for dir in [(-1, -1), (-1, 0), (-1, +1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]:
            pos = (self.position[0] + dir[0], self.position[1] + dir[1])
            if pos in other_elfs:
                all_clear = False

        if all_clear:
            return next_position

        
        for i in range(4):
            index = (i + self.offset) % 4
            pos_0 = (self.position[0] + NEXT_POSITIONS[index][0][0], self.position[1] + NEXT_POSITIONS[index][0][1])
            pos_1 = (self.position[0] + NEXT_POSITIONS[index][1][0], self.position[1] + NEXT_POSITIONS[index][1][1])
            pos_2 = (self.position[0] + NEXT_POSITIONS[index][2][0], self.position[1] + NEXT_POSITIONS[index][2][1])

            if pos_0 not in other_elfs and pos_1 not in other_elfs and pos_2 not in other_elfs:
                next_position = (self.position[0] + NEXT_POSITIONS[index][3][0], self.position[1] + NEXT_POSITIONS[index][3][1])
                break

        return next_position


class Day23(Table):

    def __init__(self):
        self.day = 23
        self.title = "Unstable Diffusion"
        self.input = self.getInput(self.day)

        self.elfs = []

    def load_elfs(self):
        self.elfs = []
        for y, line in enumerate(self.input.splitlines()):
            for x, val in enumerate(line):
                if val == '#':
                    self.elfs.append(Elf((x, y)))

    def round(self):
        elf_positions = set([elf.position for elf in self.elfs])

        moved = False
        proposed_positions = {}
        for elf in self.elfs:
            next_pos = elf.next_position(elf_positions)
            if next_pos != elf.position:
                moved = True

            if next_pos not in proposed_positions:
                proposed_positions[next_pos] = [elf]
            else:
                proposed_positions[next_pos].append(elf)

        for position in proposed_positions:
            if len(proposed_positions[position]) == 1:
                elf = proposed_positions[position][0]
                elf.position = position

        for elf in self.elfs:
            elf.offset += 1

        return moved


    def solve(self):
        start_time = time()

        self.load_elfs()
        self.image().save(self.visual_path('init.png'))

        rounds = 0
        did_move = True
        while did_move:
            did_move = self.round()
            rounds += 1

            if rounds == 10:
                elf_positions = set([elf.position for elf in self.elfs])
                max_x = max([pos[0] for pos in elf_positions])
                max_y = max([pos[1] for pos in elf_positions])
                min_x = min([pos[0] for pos in elf_positions])
                min_y = min([pos[1] for pos in elf_positions])

                diff_x = max_x - min_x + 1
                diff_y = max_y - min_y + 1

                part1 = (diff_x * diff_y) - len(elf_positions)

        part2 = rounds

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, bounds: tuple = None):
        if bounds is None:
            elf_positions = set([elf.position for elf in self.elfs])
            max_x = max([pos[0] for pos in elf_positions])
            max_y = max([pos[1] for pos in elf_positions])
            min_x = min([pos[0] for pos in elf_positions])
            min_y = min([pos[1] for pos in elf_positions])
            bounds = (min_x, max_x, min_y, max_y)

        img = Image.new('RGB', (bounds[1] - bounds[0] + 1, bounds[3] - bounds[2] + 1), 'black')
        pixels = img.load()
        for elf in self.elfs:
            pixels[elf.position[0] - bounds[0], elf.position[1] - bounds[2]] = (255, 255, 255)

        return img


if __name__ == "__main__":
    day = Day23()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
