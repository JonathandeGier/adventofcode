from Table import Table
from time import time

class Item:
    def __init__(self, value):
        self.value = value
        self.next = None

class Day17(Table):

    def __init__(self):
        self.day = 17
        self.title = "Spinlock"
        self.input = int(self.getInput(self.day).strip())

        self.part1 = ''

    def spinlock(self, steps):
        head = Item(0)
        head.next = head
        current_item = head

        for i in range(1, steps + 1):
            if i % 10_000 == 0:
                self.printRow((self.day, self.title, self.part1, str(round((i / steps) * 100, 2)) + ' %', ''), end="\r")

            for _ in range(self.input):
                current_item = current_item.next

            new_item = Item(i)
            new_item.next = current_item.next
            current_item.next = new_item

            current_item = current_item.next

        return head, current_item
        

    def solve(self):
        start_time = time()

        head, item = self.spinlock(2017)

        self.part1 = item.next.value

        head, item = self.spinlock(50_000_000)
        part2 = head.next.value

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, self.part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day17()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
