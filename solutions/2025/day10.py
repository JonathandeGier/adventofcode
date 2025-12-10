from Table import Table
from time import time
from collections import deque
import z3
      

class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Factory"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        machines = []
        for line in self.input.splitlines():
            lamps = ''
            buttons = []
            joltage = ''
            for segment in line.split(' '):
                if segment[0] == '[':
                    lamps = segment
                elif segment[0] == '(':
                    buttons.append(segment)
                elif segment[0] == '{':
                    joltage = segment
                            
            machine = {}
            machine['required_lamps'] = tuple(val == '#' for val in lamps[1:-1])
            machine['required_joltage'] = tuple(int(val) for val in joltage[1:-1].split(','))
            machine['buttons'] = tuple(tuple(int(x) for x in button[1:-1].split(',')) for button in buttons)

            machines.append(machine)


        part1 = 0
        part2 = 0
        for machine in machines:
            # Part 1
            visited = set()
            lamps = tuple(False for _ in machine['required_lamps'])
            queue = deque([(lamps, 0)])
            while queue:
                lamps, steps = queue.popleft()

                if lamps in visited:
                    continue

                visited.add(lamps)

                if lamps == machine['required_lamps']:
                    part1 += steps
                    break

                for button in machine['buttons']:
                    new_lamps = list(lamps)
                    for i in button:
                        new_lamps[i] = not new_lamps[i]

                    new_lamps = tuple(new_lamps)
                    if new_lamps in visited:
                        continue

                    queue.append((new_lamps, steps + 1))
            else:
                assert False, 'No combination of buttons found for lamps'

            # Part 2
            # Make variables for the number of times we need to press each button
            solver = z3.Optimize()
            unknowns = [z3.Int(str(button)) for i, button in enumerate(machine['buttons'])]
            
            # number of button presses cannot be negative
            for unknown in unknowns:
                solver.add(unknown >= 0)

            for i, jolt in enumerate(machine['required_joltage']):
                # To get a given jolt, we need the sum of the buttons that add to that jolt
                solver.add(jolt == z3.Sum([unknowns[j] for j, button in enumerate(machine['buttons']) if i in button]))
            
            # Minimize the answer
            answer = z3.Int('answer')
            solver.add(answer == z3.Sum(unknowns))
            h = solver.minimize(answer)

            # Check the model
            solver.check()
            solver.model()
            
            part2 += h.value().as_long()


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
