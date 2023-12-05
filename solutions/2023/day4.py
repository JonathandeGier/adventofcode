from Table import Table
from time import time

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Scratchcards"
        self.input = self.getInput(self.day)

    def parse_cards(self):
        cards = {}
        for line in self.input.splitlines():
            card, all_numbers = line.split(': ')
            card_number = int(card.split(' ')[-1])
            
            winning_numbers = [int(num) for num in all_numbers.split(' | ')[0].split() if num.isdigit()]
            numbers = [int(num) for num in all_numbers.split(' | ')[1].split() if num.isdigit()]
            
            cards[card_number] = (tuple(winning_numbers), tuple(numbers))
        
        return cards

    def solve(self):
        start_time = time()

        cards = self.parse_cards()
        card_copies = {}
        for card in cards:
            card_copies[card] = 1

        points = 0
        for card in cards:
            winning_numbers, numbers = cards[card]
            matches = 0
            for number in numbers:
                if number in winning_numbers:
                    matches += 1

            if matches > 0:
                points += pow(2, matches - 1)

            for i in range(1, matches + 1):
                card_copies[card + i] += card_copies[card]
            
        part1 = points
        part2 = sum(card_copies.values())

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
