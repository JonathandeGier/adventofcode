from Table import Table
from time import time
from collections import Counter
from itertools import combinations_with_replacement

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

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

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
        sorted_values = sorted(card_counts.values())

        if sorted_values == [5]:
            return FIVE_OF_A_KIND
        elif sorted_values == [1, 4]:
            return FOUR_OF_A_KIND
        elif sorted_values == [2, 3]:
            return FULL_HOUSE
        elif sorted_values == [1, 1, 3]:
            return THREE_OF_A_KIND
        elif sorted_values == [1, 2, 2]:
            return TWO_PAIR
        elif sorted_values == [1, 1, 1, 2]:
            return ONE_PAIR
        elif sorted_values == [1, 1, 1, 1, 1]:
            return HIGH_CARD
        else:
            assert False, f'Unknown hand type {sorted_values}'

    def bitshift_key(self, hand: int, cards, values: dict):
        # Generates a 24 bit integer to sort the array with
        # | x.x.x.x | x.x.x.x | x.x.x.x | x.x.x.x | x.x.x.x | x.x.x.x |
        # |   hand  |  card 1 |  card 2 |  card 3 |  card 4 |  card 5 |
        key = hand
        key = (key << 4) + values[cards[0]]
        key = (key << 4) + values[cards[1]]
        key = (key << 4) + values[cards[2]]
        key = (key << 4) + values[cards[3]]
        key = (key << 4) + values[cards[4]]

        return key

    def sort_key(self, cards: str) -> int:
        return self.bitshift_key(self.hand_type(cards), cards, CARD_VALUES)
    
    def joker_key(self, cards: str) -> int:
        normal_cards = [card for card in cards if card != 'J']
        if len(normal_cards) == 0:
            hand_type = FIVE_OF_A_KIND
        else:
            possible_jokers = combinations_with_replacement(normal_cards, len(cards) - len(normal_cards))
            hand_type = max([self.hand_type(normal_cards + list(joker_cards)) for joker_cards in possible_jokers])

        return self.bitshift_key(hand_type, cards, JOKER_VALUES)


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
