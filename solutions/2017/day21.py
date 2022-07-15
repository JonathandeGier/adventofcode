from Table import Table
from time import time

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "Fractal Art"
        self.input = self.getInput(self.day)

        self.rules = {}

    def add_rule(self, img_in: tuple, img_out: tuple):
        if img_in in self.rules and self.rules[img_in] != img_out:
            assert False

        self.rules[img_in] = img_out

    def to_tuple(self, string):
        final_arr = []
        working_arr = []
        for char in string:
            if char == '#':
                working_arr.append(True)
            elif char == '.':
                working_arr.append(False)
            elif char == '/':
                final_arr.append(tuple(working_arr))
                working_arr = []
        final_arr.append(tuple(working_arr))

        return tuple(final_arr)

    def flip(self, img: tuple) -> tuple:
        if len(img) == 2:
            return (
                (img[0][1], img[0][0]),
                (img[1][1], img[1][0]),
            )
        elif len(img) == 3:
            return (
                (img[0][2], img[0][1], img[0][0]),
                (img[1][2], img[1][1], img[1][0]),
                (img[2][2], img[2][1], img[2][0]),
            )
        else:
            assert False

    def rotate(self, img: tuple) -> tuple:
        if len(img) == 2:
            return (
                (img[1][0], img[0][0]),
                (img[1][1], img[0][1]),
            )
        elif len(img) == 3:
            return (
                (img[2][0], img[1][0], img[0][0]),
                (img[2][1], img[1][1], img[0][1]),
                (img[2][2], img[1][2], img[0][2]),
            )
        else:
            assert False

    def load_rules(self):
        for line in self.input.splitlines():
            raw_img_in, raw_img_out = line.split(' => ')

            img_in = self.to_tuple(raw_img_in)
            flipped_img_in = self.flip(img_in)

            img_out = self.to_tuple(raw_img_out)

            self.add_rule(img_in, img_out)
            for _ in range(3):
                img_in = self.rotate(img_in)
                self.add_rule(img_in, img_out)

            self.add_rule(flipped_img_in, img_out)
            for _ in range(3):
                flipped_img_in = self.rotate(flipped_img_in)
                self.add_rule(flipped_img_in, img_out)

    
    def upscale(self, img):
        # Cut the image in blocks
        unit = None
        if len(img) % 2 == 0:
            unit = 2
        elif len(img) % 3 == 0:
            unit = 3
        else:
            assert False

        blocks = []
        for i in range(0, len(img), unit):
            block_row = []
            for j in range(0, len(img), unit):
                block = []
                for k in range(unit):
                    block.append(tuple(img[i+k][j:j+unit]))
                block_row.append(tuple(block))
            blocks.append(block_row)

        # Upscale blocks based on the rules
        upscaled_blocks = [[self.rules[block] for block in block_row] for block_row in blocks]

        # Merge blocks to single image
        new_img = []
        for block_row in upscaled_blocks:
            for row_in_block in range(unit + 1):
                new_img_row = []
                for block in block_row:
                    for val in block[row_in_block]:
                        new_img_row.append(val)
                new_img.append(new_img_row)

        return new_img


    def solve(self):
        start_time = time()

        self.load_rules()

        img = [
            [False, True , False],
            [False, False, True ],
            [True , True , True ],
        ]

        for _ in range(5):
            img = self.upscale(img)

        part1 = sum([sum(row) for row in img])

        for _ in range(18 - 5):
            img = self.upscale(img)
        
        part2 = sum([sum(row) for row in img])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
