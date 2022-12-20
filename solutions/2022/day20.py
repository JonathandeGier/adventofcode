from Table import Table
from time import time

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Grove Positioning System"
        self.input = self.getInput(self.day)

    def mix(self, list: list, rounds: int = 1):
        for _ in range(rounds):
            for i in range(len(list)):
                item = [item for item in list if item['org_index'] == i][0]

                _from = item['new_index']
                new_index = _from + item['value']
                
                # index 0 and index -1 are the same, so for each time we loop around we need to shift an extra place
                shift = new_index // len(list)

                shift_dir = shift // len(list)

                shift_dir_dir = shift_dir // len(list)
                _to = (new_index + shift + shift_dir + shift_dir_dir) % len(list)
                # print(shift_dir_dir)
                
                # _to = new_index % len(list)
                # _to += (new_index // len(list))
                # _to = _to % len(list)


                if _to >_from:
                    # move everything in between forward
                    for moving_item in [moving_item for moving_item in list if moving_item['new_index'] > _from and moving_item['new_index'] <= _to]:
                        moving_item['new_index'] -= 1

                elif _to < _from:
                    # move everything in between backward
                    for moving_item in [moving_item for moving_item in list if moving_item['new_index'] >= _to and moving_item['new_index'] < _from]:
                        moving_item['new_index'] += 1
                
                item['new_index'] = _to

            # for i in range(len(list)):
            #     item = [item for item in list if item['new_index'] == i][0]
            #     print(item['value'], end=' ')
            print('mixed')

        return list

    def solve(self):
        start_time = time()

        # not -7271027221727
        # not -5152779532397
        # not 7317287803448
        # ... < x < 8288760019589
        # print((1567990243596) + (7779893620658) + (-1059123844665))

        list = [{'org_index': i, 'new_index': i, 'value': int(val) * 811589153} for i, val in enumerate(self.input.splitlines())]

        # for i in range(len(list)):
        #     item = [item for item in list if item['new_index'] == i][0]
        #     print(item['value'], end=' ')
        # print('')

        list = self.mix(list, 10)

        part1 = 0
        zero = [item for item in list if item['value'] == 0][0]
        print(zero)
        for i in [1000, 2000, 3000]:
            index = (zero['new_index'] + i) % len(list)

            value = [item for item in list if item['new_index'] == index][0]
            print(value)
            part1 += value['value']

        part2 = "None"

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
