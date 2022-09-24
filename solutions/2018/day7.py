from collections import defaultdict
from Table import Table
from time import time

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "The Sum of Its Parts"
        self.input = self.getInput(self.day)

    def get_steps(self):
        connections = [(line.split(' ')[1], line.split(' ')[7]) for line in self.input.splitlines()]
        unique_steps = set([conn[0] for conn in connections] + [conn[1] for conn in connections])

        steps = {}
        for letter in unique_steps:
            steps[letter] = {'req': []}

        for connection in connections:
            steps[connection[1]]['req'].append(connection[0])
        
        return steps

    def solve(self):
        start_time = time()

        steps = self.get_steps()
        order = []
        while len(steps) > 0:
            possible_steps = [step for step in steps.items() if len(step[1]['req']) == 0]
            letters = sorted([step[0] for step in possible_steps])
            order.append(letters[0])

            del steps[letters[0]]

            for key in steps:
                if letters[0] in steps[key]['req']:
                    steps[key]['req'].remove(letters[0])

        part1 = ''.join(order)

        seconds = 0
        workers = [
            {'current': None, 'cooldown': 0}, 
            {'current': None, 'cooldown': 0}, 
            {'current': None, 'cooldown': 0}, 
            {'current': None, 'cooldown': 0}, 
            {'current': None, 'cooldown': 0},
        ]
        steps = self.get_steps()
        
        done = False
        while not done:
            # decrement cooldown
            for worker in workers:
                worker['cooldown'] = worker['cooldown'] - 1

            # deassign workers
            completed = []
            for worker in workers:
                if worker['cooldown'] <= 0:
                    if worker['current'] != None:
                        completed.append(worker['current'])
                    worker['current'] = None

            # remove completed steps
            for step in completed:
                del steps[step]

                for key in steps:
                    if step in steps[key]['req']:
                        steps[key]['req'].remove(step)

            # Get possible steps
            possible_steps = sorted([step[0] for step in steps.items() if len(step[1]['req']) == 0])
            for worker in workers:
                if worker['current'] in possible_steps:
                    possible_steps.remove(worker['current'])

            # assign workers
            for worker in workers:
                if len(possible_steps) > 0 and worker['current'] is None:
                    worker['current'] = possible_steps[0]
                    worker['cooldown'] = ord(possible_steps[0]) - 4
                    possible_steps.remove(possible_steps[0])

            seconds = seconds + 1
            done = len(steps) == 0

        part2 = seconds - 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
