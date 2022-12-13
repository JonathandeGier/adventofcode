from Table import Table
from time import time
import functools

class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Distress Signal"
        self.input = self.getInput(self.day)

    def get_pairs(self):
        pairs = {}
        for i, raw_pair in enumerate(self.input.split('\n\n')):
            signal1, signal2 = raw_pair.splitlines()
            pairs[i+1] = (eval(signal1), eval(signal2))

        return pairs

    def compare(self, left, right):
        # print('compare ' + str(left) + ' vs ' + str(right))

        if type(left) == int and type(right) == int:
            if left < right:
                return -1
            elif left > right:
                return 1
            return 0
        elif type(left) == list and type(right) == list:
            for i in range(len(left)):
                if i >= len(right):
                    # print('right side ran out of items')
                    return 1
                result = self.compare(left[i], right[i])
                if result != 0:
                    return result

            if len(left) == len(right):
                return 0
            return -1
        elif type(left) == int and type(right) == list:
            # print('mixed types, convert left to ' + str([left]))
            return self.compare([left], right)
        elif type(left) == list and type(right) == int:
            # print('mixed types, convert right to ' + str([right]))
            return self.compare(left, [right])
        else:
            assert 1

    def solve(self):
        start_time = time()

        pairs = self.get_pairs()
        
        right_orders = []
        for index in pairs:
            pair = pairs[index]
            # print('Pair:', index)
            if self.compare(pair[0], pair[1]) == -1:
                right_orders.append(index)
                # print(True)
            # print('')

        part1 = sum(right_orders)

        signals = [signal[0] for signal in pairs.values()] + [signal[1] for signal in pairs.values()]
        signals.append([[2]])
        signals.append([[6]])

        signals = sorted(signals, key=functools.cmp_to_key(self.compare))
        
        part2 = 1
        for i, signal in enumerate(signals):
            if signal == [[2]] or signal == [[6]]:
                part2 *= (i + 1)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
