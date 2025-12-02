from Table import Table
from time import time

class Day0(Table):

    def __init__(self):
        self.day = 2
        self.title = "Gift Shop"
        self.input = self.getInput(self.day)

    def is_valid_p1(self, num: int) -> bool:
        num = str(num)
        # for seq_size in range(1, (len(num) // 2) + 1):
        #     for i in range(len(num) - seq_size):
        #         if num[i:i+seq_size] == num[i+seq_size:i+seq_size+seq_size]:
        #             return False

        if len(num) % 2 != 0:
            return True
        
        midpoint = len(num) // 2
        if num[:midpoint] == num[midpoint:]:
            return False
                
        return True
    
    def is_valid_p2(self, num: int) -> bool:
        num = str(num)
        for seq_size in range(1, (len(num) // 2) + 1):
            if len(num) % seq_size != 0:
                continue

            segment = num[:seq_size]
            all_same = True
            for _start in range(0, len(num), seq_size):
                if num[_start:_start + seq_size] != segment:
                    all_same = False
                    break

            if all_same:
                return False
            
        return True


    def solve(self):
        start_time = time()

        part1 = 0
        part2 = 0
        ranges = self.input.split(',')
        for _range in ranges:
            _start, _end = [int(x) for x in _range.split('-')]

            for num in range(_start, _end + 1):
                if not self.is_valid_p1(num):
                    part1 += num

                if not self.is_valid_p2(num):
                    # print(num)
                    part2 += num


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day0()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
