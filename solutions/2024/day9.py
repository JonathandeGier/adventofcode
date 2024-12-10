from Table import Table
from time import time

class Day9(Table):

    def __init__(self):
        self.day = 9
        self.title = "Disk Fragmenter"
        self.input = self.getInput(self.day)

    def expand_diskmap(self):
        blocks = []
        for i, val in enumerate(self.input.strip()):
            is_file = i / 2 == i // 2
            file_id = i // 2
            for _ in range(int(val)):
                blocks.append(file_id if is_file else '.')
        return blocks
        

    def solve(self):
        start_time = time()

        blocks = self.expand_diskmap()
        index = 0
        while '.' in blocks:
            block = blocks.pop()
            if block == '.':
                continue

            index = blocks.index('.', index)
            blocks[index] = block
        part1 = sum([i * val for i, val in enumerate(blocks) if val != '.' and val != None])


        blocks = self.expand_diskmap()
        file_start = len(blocks) - 1
        file_end = len(blocks) - 1
        for file_id in range(blocks[-1], -1, -1):
            # find the start and end of the file
            pointer = file_end
            while blocks[pointer] != file_id:
                pointer -= 1

            file_end = pointer
            while blocks[pointer] == file_id:
                pointer -= 1
            file_start = pointer + 1

            size = file_end - file_start + 1

            # find the first available free spot from the start of the file
            index = 0
            while True:
                try:
                    index = blocks.index('.', index, file_start)
                    free = all(val == '.' for val in blocks[index:index + size])
                    if free:
                        break
                    else:
                        index += 1
                except ValueError:
                    free = False
                    break

            if not free:
                continue

            # move the file blocks
            for i in range(size):
                blocks[file_start + i] = '.'
                blocks[index + i] = file_id
    
        part2 = sum([i * val for i, val in enumerate(blocks) if val != '.'])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day9()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
