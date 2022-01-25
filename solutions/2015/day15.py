from Table import Table
from time import time

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Science for Hungry People"
        self.input = self.getInput(self.day)

    def get_ingrediants(self):
        ingrediants = []
        for line in self.input.splitlines():
            segemnts = line.split(" ")
            capacity = int(segemnts[2][:len(segemnts[2]) - 1])
            durability = int(segemnts[4][:len(segemnts[4]) - 1])
            flavor = int(segemnts[6][:len(segemnts[6]) - 1])
            texture = int(segemnts[8][:len(segemnts[8]) - 1])
            calories = int(segemnts[10])
            ingrediants.append([capacity, durability, flavor, texture, calories])
        return ingrediants

    # https://stackoverflow.com/questions/7748442/generate-all-possible-lists-of-length-n-that-sum-to-s-in-python
    def percentages(self, length, total_sum):
        if length == 1:
            yield (total_sum,)
        else:
            for value in range(total_sum + 1):
                for permutation in self.percentages(length - 1, total_sum - value):
                    yield (value,) + permutation

    def calculate_score(self, ingrediants, percentages):
        property_scores = [0, 0, 0, 0]

        for i, percentage in enumerate(percentages):
            for j, property in enumerate(ingrediants[i]):
                if j == len(ingrediants[i]) - 1:
                    continue
                property_scores[j] += (percentage * property)

        for i, val in enumerate(property_scores):
            if val < 0:
                property_scores[i] = 0

        return property_scores[0] * property_scores[1] * property_scores[2] * property_scores[3]

    def calories(self, ingrediants, percentages):
        calories = 0

        for i, percentage in enumerate(percentages):
            calories += (percentage * ingrediants[i][4])
        
        return calories


    def solve(self):
        start_time = time()

        ingrediants = self.get_ingrediants()

        possebilities = list(self.percentages(len(ingrediants), 100))
        
        best_score = 0
        best_calories = 0
        for possebility in possebilities:
            score = self.calculate_score(ingrediants, possebility)
            if score > best_score:
                best_score = score

            if score > best_calories and self.calories(ingrediants, possebility) == 500:
                best_calories = score

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, best_score, best_calories, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
