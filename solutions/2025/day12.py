from Table import Table
from time import time

import cv2
from numpy import asarray

VISITED = set()

class Day12(Table):

    def __init__(self):
        self.day = 12
        self.title = "Christmas Tree Farm"
        self.input = self.getInput(self.day)

        self.make_visuals = __name__ == '__main__'
        self.video = None
        self.fps = 60

    def solve(self):
        start_time = time()

        # Input parsing
        shapes = []
        regions = []
        for segment in self.input.split('\n\n'):
            shape = set()
            for y, line in enumerate(segment.splitlines()):
                if 'x' in line:
                    size, required_shapes = line.split(': ')
                    _x, _y = size.split('x')
                    regions.append(((int(_x), int(_y)), tuple(int(count) for count in required_shapes.split())))

                if ':' in line:
                    continue

                for x, val in enumerate(line):
                    if val == '#':
                        shape.add((x, y-1))

            if len(shape) > 0:
                # print(shape)
                shapes.append(shape)

        # print(regions)

        # Compute every rotation and flip of the shapes
        shape_variants = []
        for shape in shapes:
            variants = set()

            prev_shape_variant = shape
            for _ in range(4):
                rotated = []
                # clockwise rotation"
                for pos in prev_shape_variant:
                    if pos[1] == 0:
                        x = 2
                    elif pos[1] == 2:
                        x = 0
                    else:
                        x = 1

                    rotated.append((x, pos[0]))

                flipped_x = []
                for pos in rotated:
                    if pos[1] == 0:
                        y = 2
                    elif pos[1] == 2:
                        y = 0
                    else:
                        y = 1
                    flipped_x.append((pos[0], y))

                flipped_y = []
                for pos in rotated:
                    if pos[0] == 0:
                        x = 2
                    elif pos[0] == 2:
                        x = 0
                    else:
                        x = 1
                    flipped_y.append((x, pos[1]))

                variants.add(tuple(sorted(rotated)))
                variants.add(tuple(sorted(flipped_x)))
                variants.add(tuple(sorted(flipped_y)))

                prev_shape_variant = rotated

            shape_variants.append(tuple(variants))
            # print(len(variants))

        # There is an actual algorithm for packing the shapes in a small area, but it is too slow for the input
        # for size, required_shapes in regions[0:1]:
        #     if self.make_visuals:
        #         img = self.image_region(size)
        #         self.video = cv2.VideoWriter(self.visual_path('part1.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), self.fps, img.size)
        #         self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        #     print(size, required_shapes)
        #     applied_shapes = self.apply_shapes(size, required_shapes, shape_variants)

        #     if self.make_visuals:
        #         img = self.image_region(size, shape_variants, applied_shapes)
        #         for _ in range(self.fps * 10):
        #             self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))
                
        #         self.video.release()
        #         cv2.destroyAllWindows()


        # The input can actually be solved by checking if the area is big enough to fit the required shapes without overlapping
        part1 = 0
        for size, required_shapes in regions:
            if size[0] * size[1] >= sum(required_shapes) * 9:
                part1 += 1

        part2 = "Finish decorating the North Pole"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def apply_shapes(self, size, required_shapes, shape_variants, applied_shapes = [], applied_mask = set(), visited = set()):
        # 1. count the applied shapes
        shape_count = [0 for _ in range(len(shape_variants))]
        for shape_i, variant_i, offset in applied_shapes:
            shape_count[shape_i] += 1

        all_applied = True
        for shape_i, count in enumerate(required_shapes):
            if shape_count[shape_i] != count:
                all_applied = False
                break
        
        if all_applied:
            return applied_shapes
        
        applied_hash = tuple(sorted(applied_shapes))
        if applied_hash in visited:
            return None
        
        # 2. Determine shapes to apply
        shapes_to_apply = []
        for shape_i, count in enumerate(required_shapes):
            if shape_count[shape_i] < count:
                shapes_to_apply.append(shape_i)

        for shape_i in shapes_to_apply:
            for variant_i, variant in enumerate(shape_variants[shape_i]):
                # Determine location to apply shape
                for x in range(size[0] - 2):
                    for y in range(size[1] - 2):
                        offset_possible = True
                        for pos in variant:
                            applied_pos = (pos[0] + x, pos[1] + y)
                            if applied_pos in applied_mask:
                                offset_possible = False
                                break

                            # size requirement
                            if applied_pos[0] >= size[0] or applied_pos[1] >= size[1]:
                                offset_possible = False
                                break

                        if not offset_possible:
                            continue

                        new_applied_mask = applied_mask.copy()
                        new_applied_shapes = applied_shapes.copy()

                        new_visited = visited.copy()
                        # new_visited.add(applied_hash)

                        for pos in variant:
                            applied_pos = (pos[0] + x, pos[1] + y)
                            new_applied_mask.add(applied_pos)

                        new_applied_shapes.append((shape_i, variant_i, (x, y)))

                        if self.make_visuals:
                            img = self.image_region(size, shape_variants, new_applied_shapes)
                            self.video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

                        result = self.apply_shapes(size, required_shapes, shape_variants, new_applied_shapes, new_applied_mask, new_visited)
                        if result != None:
                            return result
                    
        return None

    
    def image_shape(self, shape):
        data = {}
        for pos in shape:
            data[pos] = '#'

        return self.image_map(data, {'#': (255, 255, 255)}, scale=20)
    
    def image_region(self, size, shape_variants = [], applied_shapes = []):
        data = {}
        for x in range(size[0]):
            for y in range(size[1]):
                data[x, y] = '.'

        for shape_i, variant_i, offset in applied_shapes:
            for pos in shape_variants[shape_i][variant_i]:
                applied_pos = (pos[0] + offset[0], pos[1] + offset[1])
                data[applied_pos] = shape_i

        return self.image_map(data, {
            0: (255, 0, 0),
            1: (0, 255, 0),
            2: (0, 0, 255),
            3: (255, 255, 0),
            4: (0, 255, 255),
            5: (255, 0, 255),
        }, scale=15)



if __name__ == "__main__":
    day = Day12()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
