from Table import Table
from time import time
from PIL import Image
import cv2
from numpy import asarray

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Cathode-Ray Tube"
        self.input = self.getInput(self.day)

        self.make_video = False
        self.video = None

    def get_instructions(self):
        instructions = []
        for line in self.input.splitlines():
            segments = line.split(' ')
            if len(segments) == 2:
                instructions.append((segments[0], int(segments[1])))
            else:
                instructions.append((segments[0], ''))

        return instructions

    def run(self, instructions: list):
        cycle = 1
        sub_cycle = 0
        instruction_pointer = 0
        x = 1
        row = 0
        lit_pixels = []
        signals = []

        if self.make_video:
            img = self.image(lit_pixels)
            self.video = cv2.VideoWriter(self.visual_path('render.mp4'), cv2.VideoWriter_fourcc(*'MP4V'), 30, img.size)
            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        while True:
            if instruction_pointer < 0 or instruction_pointer >= len(instructions):
                break

            if (cycle + 20) % 40 == 0:
                signals.append(cycle * x)

            # CRT
            pixel = ((cycle - 1) % 40, row)
            if pixel[0] == x or pixel[0] == x - 1 or pixel[0] == x + 1:
                lit_pixels.append(pixel)

            if cycle % 40 == 0:
                row += 1

            if self.make_video:
                img = self.image(lit_pixels)
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

            # Execute instruction
            instruction = instructions[instruction_pointer]
            if instruction[0] == 'noop':
                cycle += 1
                instruction_pointer += 1
            elif instruction[0] == 'addx':
                cycle += 1
                if sub_cycle == 0:
                    sub_cycle = 1
                else:
                    sub_cycle = 0
                    x += instruction[1]
                    instruction_pointer += 1
            else:
                assert False

        # save image answer
        img = self.image(lit_pixels)
        img.save(self.visual_path('display.png'))

        # make last video frames and save
        if self.make_video:
            for _ in range(150):
                self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
            cv2.destroyAllWindows()
            self.video.release()

        return signals


    def solve(self):
        start_time = time()

        instructions = self.get_instructions()

        part1 = sum(self.run(instructions))
        part2 = "visuals/day10/display.png"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


    def image(self, lit_pixels: list):
        img = Image.new('RGB', (40, 6), 'black')
        pixels = img.load()
        for pixel in lit_pixels:
            pixels[pixel] = (200, 200, 200)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
