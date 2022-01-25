from itertools import permutations
from Table import Table
from time import time

class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Knights of the Dinner Table"
        self.input = self.getInput(self.day)

    def get_preferences(self):
        preferences = {}
        names = []
        for line in self.input.splitlines():
            segments = line[:len(line) - 1].split(" ")
            personA = segments[0]
            personB = segments[-1]
            amount = int(segments[3])
            if segments[2] == "lose":
                amount *= -1

            if personA not in preferences:
                preferences[personA] = {personB: amount}
                names.append(personA)
            else:
                preferences[personA][personB] = amount
        return preferences, names


    def total_happiness(self, arrangement, preferences):
        total_happiness = 0
        for i, person in enumerate(arrangement):
            left = i - 1
            right = i + 1
            if right == len(arrangement):
                right = 0

            total_happiness += preferences[person][arrangement[left]]
            total_happiness += preferences[person][arrangement[right]]
        return total_happiness

    def solve(self):
        start_time = time()

        preferences, names = self.get_preferences()
    
        
        max_happiness = 0
        for arrangement in permutations(names):
            happiness = self.total_happiness(arrangement, preferences)
            if happiness > max_happiness:
                max_happiness = happiness
        part1 = max_happiness

        me = "me"
        names.append(me)
        my_preferences = {}
        for person in preferences.keys():
            preferences[person][me] = 0
            my_preferences[person] = 0
        preferences[me] = my_preferences
        
        max_happiness = 0
        for arrangement in permutations(names):
            happiness = self.total_happiness(arrangement, preferences)
            if happiness > max_happiness:
                max_happiness = happiness
        part2 = max_happiness

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
