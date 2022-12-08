from Table import Table
from time import time
import numpy as np
from PIL import Image

class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Treetop Tree House"
        self.input = self.getInput(self.day)

        self.map = None

    def load_map(self):
        self.map = np.array([[int(val) for val in line] for line in self.input.splitlines()])

    def calculate_visables(self, tree: int, trees) -> int:
        visible = 0
        for other_tree in trees:
            if other_tree < tree:
                visible += 1
            else:
                visible += 1
                break
        return visible

    def solve(self):
        start_time = time()

        self.load_map()

        visible = 0

        # all trees on the edge are visible
        visible += (len(self.map[0]) * 2)
        visible += (len(self.map[:, 0]) * 2) - 4

        visables = set()

        for i, row in enumerate(self.map):
            if i == 0 or i == len(self.map) - 1:
                continue

            for j, tree in enumerate(row):
                if j == 0 or j == len(row) - 1:
                    continue

                max_north = max(self.map[:, j][:i])
                max_south = max(self.map[:, j][i+1:])
                max_east = max(self.map[i][:j])
                max_west = max(self.map[i][j+1:])

                tree_visible = tree > max_north or tree > max_south or tree > max_east or tree > max_west
                if tree_visible:
                    visables.add((i, j))
                    visible += 1

        part1 = visible

        part2 = 0
        best = (-1, -1)
        for i, row in enumerate(self.map):
            if i == 0 or i == len(self.map) - 1:
                continue

            for j, tree in enumerate(row):
                if j == 0 or j == len(row) - 1:
                    continue

                up = self.map[:, j][:i][::-1]
                down = self.map[:, j][i+1:]
                left = self.map[i][:j][::-1]
                right = self.map[i][j+1:]

                up_visible = self.calculate_visables(tree, up)
                down_visible = self.calculate_visables(tree, down)
                left_visible = self.calculate_visables(tree, left)
                right_visible = self.calculate_visables(tree, right)

                score = up_visible * down_visible * left_visible * right_visible

                if score > part2:
                    part2 = score
                    best = (i, j)

        end_time = time()
        seconds_elapsed = end_time - start_time

        self.image(visables, best).save(self.visual_path('map.png'))

        return (self.day, self.title, part1, part2, seconds_elapsed)

    def image(self, visables: set, best: tuple):
        
        img = Image.new('RGB', self.map.shape, 'black')
        pixels = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if (x, y) == best:
                    pixels[x, y] = (0, 0, 200)
                elif (x, y) in visables or x == 0 or y == 0 or x == img.size[0] - 1 or y == img.size[1] - 1:
                    pixels[x, y] = (0, self.map[x][y] * 20, 0)
                else:
                    val = self.map[x][y] * 20
                    pixels[x, y] = (val, val, val)

        scale = 10
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)

        return img

if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
