from Table import Table
from time import time
from collections import deque

class Day11(Table):

    def __init__(self):
        self.day = 11
        self.title = ""
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        # Input parsing
        devices = {}
        for line in self.input.splitlines():
            device, connected = line.split(': ')
            devices[device] = tuple(c for c in connected.split(' '))

        # svr: rqx hlx yqu ixr
        #   rqx: odx fcf csa cmm rcj qcs prp pmj
        #   hlx: kaf odx cmm xry rsn tun prp csa gxr bcy opw fts dvi rcj
        #   yqu: xry tun qcs prp odx kaf cmm csa gxr bcy opw dvi fts
        #   ixr: orj pmj xry dvi bcy cmm gxr csa

        # Part 1
        part1 = 0
        # queue = deque(['you'])
        # while queue:
        #     device = queue.popleft()

        #     if device == 'out':
        #         part1 += 1
        #         continue

        #     for other_device in devices[device]:
        #         queue.append(other_device)

        # Part 2
        # todo cache: from x to y: n steps
        part2 = 0
        queue = deque([('svr', [])])
        while queue:
            device, path = queue.popleft()

            if device == 'out':
                if 'fft' in path and 'dac' in path:
                    part2 += 1
                continue

            print(len(path), path)

            for other_device in devices[device]:
                new_path = path.copy()
                if other_device in path:
                    continue

                new_path.append(other_device)

                queue.append((other_device, new_path))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day11()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
