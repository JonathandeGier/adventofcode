from Table import Table
from time import time
from collections import deque

import cv2
from numpy import asarray

WALL = '#'
BOX = 'O'
EMPTY = '.'
BOT = '@'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

BOX_LEFT = '['
BOX_RIGHT = ']'

DIRS = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

COLORS = {
    WALL: (255, 255, 255),
    BOX: (150, 75, 0),
    BOT: (100, 100, 100),
    BOX_LEFT: (150, 75, 0),
    BOX_RIGHT: (150, 75, 0),
}

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Warehouse Woes"
        self.input = self.getInput(self.day)

        self.map = None
        self.pos = None
        self.moves = None

        self.make_visuals = __name__ == '__main__'

    def parse_map(self):
        map_data, move_data = self.input.split('\n\n')
        self.map = {}
        for y, line in enumerate(map_data.splitlines()):
            for x, val in enumerate(line):
                if val == BOT:
                    self.pos = (x, y)
                self.map[x, y] = val
        
        self.moves = []
        for line in move_data.splitlines():
            for move in line:
                self.moves.append(move)

    def parse_wide_map(self):
        map_data, _ = self.input.split('\n\n')
        self.map = {}
        for y, line in enumerate(map_data.splitlines()):
            wide_line = []
            for val in line:
                if val == WALL:
                    wide_line.append(WALL)
                    wide_line.append(WALL)
                elif val == BOX:
                    wide_line.append(BOX_LEFT)
                    wide_line.append(BOX_RIGHT)
                elif val == EMPTY:
                    wide_line.append(EMPTY)
                    wide_line.append(EMPTY)
                elif val == BOT:
                    wide_line.append(BOT)
                    wide_line.append(EMPTY)
            
            for x, val in enumerate(wide_line):
                if val == BOT:
                    self.pos = (x, y)
                self.map[x, y] = val


    def move(self, pos: tuple, dir: str) -> bool:
        diff = DIRS[dir]
        next_pos = (pos[0] + diff[0], pos[1] + diff[1])

        def map_move():
            if self.map[pos] == BOT:
                self.pos = next_pos
            self.map[next_pos] = self.map[pos]
            self.map[pos] = EMPTY

        if self.map[next_pos] == WALL:
            return False
        elif self.map[next_pos] == EMPTY:
            map_move()
            return True
        elif self.move(next_pos, dir):
            map_move()
            return True
        
    def move_wide(self, pos: tuple, dir: str) -> bool:
        # Left/Right can be handled by part 1 code
        if dir == LEFT or dir == RIGHT:
            return self.move(pos, dir)

        diff = DIRS[dir]

        # Find all the tiles that are moved at once
        queue = deque([pos])
        move_block = set()
        next_tiles = set()
        while len(queue) > 0:
            _pos = queue.popleft()
            
            if _pos in move_block:
                continue
            move_block.add(_pos)

            if self.map[_pos] == BOX_LEFT:
                queue.append((_pos[0] + DIRS[RIGHT][0], _pos[1] + DIRS[RIGHT][1]))
            elif self.map[_pos] == BOX_RIGHT:
                queue.append((_pos[0] + DIRS[LEFT][0], _pos[1] + DIRS[LEFT][1]))

            _next_pos = (_pos[0] + diff[0], _pos[1] + diff[1])
            if self.map[_next_pos] == BOX_LEFT or self.map[_next_pos] == BOX_RIGHT:
                queue.append(_next_pos)
            else:
                next_tiles.add(self.map[_next_pos])

        # Tiles cannot be moved because one of the tiles in the block is in front of a wall
        if WALL in next_tiles:
            return False
        
        assert EMPTY in next_tiles and len(next_tiles) == 1

        tiles = sorted(move_block, key=lambda tile: (tile[1], tile[0]), reverse=True if diff[1] == 1 else False)
        
        for tile in tiles:
            next_tile = (tile[0] + diff[0], tile[1] + diff[1])
            if self.map[tile] == BOT:
                self.pos = next_tile
            self.map[next_tile] = self.map[tile]
            self.map[tile] = EMPTY

    def solve(self):
        start_time = time()

        # Part 1
        self.parse_map()

        video = None
        if self.make_visuals:
            img = self.image_map(self.map, COLORS, scale=10)
            img.save(self.visual_path('part1_start.png'))
            video = cv2.VideoWriter(self.visual_path('part1.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 30, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        frame = 0
        for direction in self.moves:
            self.move(self.pos, direction)

            if frame < 1800:
                self.frame(video)
            frame += 1
            if frame == 1800 and self.make_visuals:
                video.release()
                cv2.destroyAllWindows()

        part1 = sum([pos[0] + pos[1] * 100 for pos, val in self.map.items() if val == BOX])
        if self.make_visuals:
            self.image_map(self.map, COLORS, scale=10).save(self.visual_path('part1_end.png'))

        # Part 2
        self.parse_wide_map()

        if self.make_visuals:
            img = self.image_map(self.map, COLORS, scale=10)
            img.save(self.visual_path('part2_start.png'))
            video = cv2.VideoWriter(self.visual_path('part2.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 30, img.size)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))

        frame = 0
        for direction in self.moves:
            self.move_wide(self.pos, direction)

            if frame < 1800:
                self.frame(video)
            frame += 1
            if frame == 1800 and self.make_visuals:
                video.release()
                cv2.destroyAllWindows()

        part2 = sum([pos[0] + pos[1] * 100 for pos, val in self.map.items() if val == BOX_LEFT])
        if self.make_visuals:
            self.image_map(self.map, COLORS, scale=10).save(self.visual_path('part2_end.png'))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    
    def frame(self, video):
        if self.make_visuals:
            img = self.image_map(self.map, COLORS, scale=10)
            video.write(cv2.cvtColor(asarray(img), cv2.COLOR_BGR2RGB))


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
