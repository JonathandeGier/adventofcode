from Table import Table
from time import time
from collections import Counter
from itertools import product

CARD_VALUES = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13,
}

JOKER_VALUES = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 11,
    'K': 12,
    'A': 13,
}

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Camel Cards"
        self.input = self.getInput(self.day)

        self.hands = {}

    def parse_hands(self):
        self.hands = {}
        for line in self.input.splitlines():
            cards, bid = line.split(' ')
            self.hands[cards] = int(bid)

        assert len(self.hands) == len(self.input.splitlines()), "Not all hands are unique"

    def hand_type(self, cards) -> int:
        card_counts = Counter(cards)
        card_values = card_counts.values()
        value_counts = Counter(card_values)

        if len(card_values) == 1 and value_counts[5] == 1:
            return 7 # five of a kind
        elif len(card_values) == 2 and 4 in card_values:
            return 6 # four of a kind
        elif len(card_values) == 2 and 3 in card_values and 2 in card_values:
            return 5 # Full house
        elif len(card_values) == 3 and 3 in card_values:
            return 4 # three of a kind
        elif len(card_values) == 3 and value_counts[2] == 2:
            return 3 # Two pair
        elif len(card_values) == 4 and value_counts[2] == 1:
            return 2 # One Pair
        else:
            return 1 # High card

    def sort_key(self, cards: str) -> tuple:
        return (self.hand_type(cards), CARD_VALUES[cards[0]], CARD_VALUES[cards[1]], CARD_VALUES[cards[2]], CARD_VALUES[cards[3]], CARD_VALUES[cards[4]])
    
    def joker_key(self, cards: str) -> tuple:
        normal_cards = [card for card in cards if card != 'J']
        if len(normal_cards) == 0:
            hand_type = 7
        else:
            possible_jokers = product(normal_cards, repeat=len(cards) - len(normal_cards))
            hand_type = max([self.hand_type(normal_cards + list(joker_cards)) for joker_cards in possible_jokers])

        return (hand_type, JOKER_VALUES[cards[0]], JOKER_VALUES[cards[1]], JOKER_VALUES[cards[2]], JOKER_VALUES[cards[3]], JOKER_VALUES[cards[4]])


    def solve(self):
        start_time = time()

        self.parse_hands()

        sorted_hands = sorted([cards for cards in self.hands.keys()], key=self.sort_key)
        part1 = sum([(rank + 1) * self.hands[cards] for rank, cards in enumerate(sorted_hands)])
        
        sorted_hands = sorted([cards for cards in self.hands.keys()], key=self.joker_key)
        part2 = sum([(rank + 1) * self.hands[cards] for rank, cards in enumerate(sorted_hands)])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
