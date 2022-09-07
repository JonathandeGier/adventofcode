from collections import defaultdict
from posixpath import split
from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "No Matter How You Slice It"
        self.input = self.getInput(self.day)

    def get_claims(self):
        claims = {}
        for line in self.input.splitlines():
            id_string, info = line.split(' @ ')
            id = int(id_string[1:])

            offset, size = info.split(': ')
            offsetx, offsety = offset.split(',')
            sizex, sizey = size.split('x')

            claim = (int(offsetx), int(offsety), int(sizex), int(sizey))
            claims[id] = claim

        return claims

    def solve(self):
        start_time = time()

        claims = self.get_claims()
        
        grid = defaultdict(lambda: [])
        no_overlap_ids = set()
        for claim_id in claims:
            claim = claims[claim_id]

            overlaps = False
            cancel_overlaps = set()
            for x in range(claim[0], claim[0] + claim[2]):
                for y in range(claim[1], claim[1] + claim[3]):
                    ids = grid[(x, y)]

                    if len(ids) > 0:
                        overlaps = True
                        for id in ids:
                            cancel_overlaps.add(id)

                    ids.append(claim_id)
            
            if not overlaps:
                no_overlap_ids.add(claim_id)

            for id in cancel_overlaps:
                if id in no_overlap_ids:
                    no_overlap_ids.remove(id)

        overlaps = 0
        for coord in grid:
            if len(grid[coord]) >= 2:
                overlaps += 1

        part1 = overlaps
        part2 = no_overlap_ids.pop()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
