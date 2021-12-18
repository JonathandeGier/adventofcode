from getInput import get_input
from itertools import permutations
import math
import copy


class NumberPair:

    def __init__(self, left, right, parent = None):
        assert type(left) == int or type(left) == NumberPair
        assert type(right) == int or type(right) == NumberPair

        self.left = left
        self.right = right
        self.parent = parent


    def depth(self):
        if self.parent == None:
            return 0
        else:
            return 1 + self.parent.depth()

    def remove_child(self, child):
        if self.left == child:
            self.left = 0
        elif self.right == child:
            self.right = 0
        else:
            print("Error removing child")


    def magnitude(self):
        if type(self.left) == NumberPair:
            left = self.left.magnitude()
        else:
            left = self.left

        if type(self.right) == NumberPair:
            right = self.right.magnitude()
        else:
            right = self.right

        return (3*left) + (2*right)


    def reduce(self):
        while True:
            did_explode = self.__explode()

            did_split = False
            if not did_explode:
                did_split = self.__split()

            if not did_explode and not did_split:
                break


    def __split(self):
        # split left child
        if type(self.left) == NumberPair:
            if self.left.__split():
                return True

        # split left
        if type(self.left) == int and self.left >= 10:
            new_left = math.floor(self.left / 2.0)
            new_right = math.ceil(self.left / 2.0)
            self.left = NumberPair(new_left, new_right, self)
            return True

        # split right child
        if type(self.right) == NumberPair:
            if self.right.__split():
                return True

        # split right
        if type(self.right) == int and self.right >= 10:
            new_left = math.floor(self.right / 2.0)
            new_right = math.ceil(self.right / 2.0)
            self.right = NumberPair(new_left, new_right, self)
            return True 

        return False


    def __explode(self):
        # explode
        if self.depth() >= 4 and type(self.left) == int and type(self.right) == int:
            self.parent.__add_to_first_left_number(self.left, self)
            self.parent.__add_to_first_right_number(self.right, self)
            self.parent.remove_child(self)
            return True

        # explode children
        if type(self.left) == NumberPair:
            if self.left.__explode():
                return True
        if type(self.right) == NumberPair:
            if self.right.__explode():
                return True

        return False


    def __add_to_first_left_number(self, x, source):
        if source == self.left and self.parent != None:
            self.parent.__add_to_first_left_number(x, self)
        elif source == self.right:
            if type(self.left) == int:
                self.left += x
            else:
                self.left.__add_to_first_left_number(x, self)
        elif self.parent != None and source == self.parent:
            if type(self.right) == int:
                self.right += x
            else:
                self.right.__add_to_first_left_number(x, self)  


    def __add_to_first_right_number(self, x, source):
        if source == self.left:
            if type(self.right) == int:
                self.right += x
            else:
                self.right.__add_to_first_right_number(x, self)
        elif self.parent != None and source == self.parent:
            if type(self.left) == int:
                self.left += x
            else:
                self.left.__add_to_first_right_number(x, self)
        elif source == self.right and self.parent != None:
            self.parent.__add_to_first_right_number(x, self)


    def __add__(self, other):
        assert type(other) == NumberPair
        left = copy.deepcopy(self)
        right = copy.deepcopy(other)

        new_pair = NumberPair(left, right)

        left.parent = new_pair
        right.parent = new_pair

        new_pair.reduce()

        return new_pair

    def __str__(self):
        return "".join(["[", str(self.left), ",", str(self.right), "]"])


def get_numbers():
    input = get_input(2021, 18).splitlines()
    numbers = []
    for line in input:
        numbers.append(parse(line))
    return numbers


def indexes_of_char(string, char):
    return [i for i, ltr in enumerate(string) if ltr == char]


def parse(string: str):
    if string[0] == "[" and string[-1] == "]":
        string = string[1:-1]
        for index in indexes_of_char(string, ","):
            left = string[:index]
            right = string[index + 1:]
            if left.count("[") == left.count("]") and right.count("[") == right.count("]"):
                left = parse(left)
                right = parse(right)

                pair = NumberPair(left, right)

                if type(left) == NumberPair:
                    left.parent = pair
                if type(right) == NumberPair:
                    right.parent = pair

                return pair
    else:
        return int(string)
    


def main():

    numbers = get_numbers()

    number = numbers[0]
    for i in range(1, len(numbers)):
        number = number + numbers[i]

    print("Puzzle 1:")
    print(number.magnitude())
    print("")

    numbers = get_numbers()
    index_combinations = list(permutations(range(len(numbers)), 2))

    max_magnitude = 0
    for i, j in index_combinations:
        number = numbers[i] + numbers[j]
        magnitude = number.magnitude()
        if magnitude > max_magnitude:
            max_magnitude = magnitude

    print("Puzzle 2:")
    print(max_magnitude)


if __name__ == "__main__":
    main()
