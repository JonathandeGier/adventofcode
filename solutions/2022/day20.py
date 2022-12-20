from Table import Table
from time import time

class Item:
    def __init__(self, index: int, value: int):
        self.index = index
        self.value = value

        self.next = None
        self.prev = None

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Grove Positioning System"
        self.input = self.getInput(self.day)

        self.items = {}
        self.length = None
        self.zero = None

    def load_items(self, p2 = False):
        self.items = {}
        for i, val in enumerate(self.input.splitlines()):
            value = int(val)

            if p2:
                value = value * 811589153
            self.items[i] = Item(i, value)

            if value == 0:
                self.zero = self.items[i]

        self.length = len(self.items.keys())
        for i in range(self.length):
            next_i = (i + 1) % self.length
            prev_i = (i - 1) % self.length

            self.items[i].next = self.items[next_i]
            self.items[i].prev = self.items[prev_i]

    def mix(self, rounds: int = 1):
        for _ in range(rounds):
            for i in range(self.length):

                item = self.items[i]

                if item.value == 0:
                    continue

                diff = abs(item.value) % (self.length - 1)
                assert diff != 0

                other_item = item
                for _ in range(diff):
                    if item.value > 0:
                        other_item = other_item.next
                    else:
                        other_item = other_item.prev

                if item.value > 0:
                    other_item = other_item.next


                # move the item to the other item
                # remove the item from its current position
                item.next.prev = item.prev
                item.prev.next = item.next

                # insert the item adter the other_item
                temp_other_prev = other_item.prev
                temp_other_next = other_item.next
                other_item.prev = item
                item.next = other_item
                item.prev = temp_other_prev
                temp_other_prev.next = item

    def printList(self):
        current = self.zero
        for _ in range(self.length):
            print(current.value, end=' ')
            current = current.next
        print('')

    def solve(self):
        start_time = time()

        self.printRow((self.day, self.title, '', '', ''), end='\r')

        self.load_items()
        self.mix()

        part1 = 0
        current = self.zero
        for _ in range(3):
            for _ in range(1000):
                current = current.next
            part1 += current.value

        self.printRow((self.day, self.title, part1, '', ''), end='\r')

        self.load_items(True)
        self.mix(10)

        part2 = 0
        current = self.zero
        for _ in range(3):
            for _ in range(1000):
                current = current.next
            part2 += current.value

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
