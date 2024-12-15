from Table import Table
from time import time
import heapq

class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Claw Contraption"
        self.input = self.getInput(self.day)

    def parse_machines(self):
        machines = []
        for machine in self.input.split('\n\n'):
            m = {}
            for line in machine.splitlines():
                name, coords = line.split(': ')
                x_str, y_str = coords.split(', ')
                x = int(x_str[2:])
                y = int(y_str[2:])

                if 'A' in name:
                    name = 'a'
                elif 'B' in name:
                    name = 'b'
                else:
                    name = 'target'

                m[name] = (x, y)
            machines.append(m)
        return machines
                

    def solve(self):
        start_time = time()

        machines = self.parse_machines()

        part1 = 0
        part2 = 0

        for machine in machines:
            for is_part2 in [False, True]:
                target = machine['target']
                a = machine['a']
                b = machine['b']

                if is_part2:
                    target = (target[0] + 10000000000000, target[1] + 10000000000000)

                # Solve for number of A presses
                y = b[0] - b[1]
                x = a[1] - a[0]
                rest = target[0] - target[1]

                if y == 0:
                    # Solve for number of B presses
                    y = a[0] - a[1]
                    x = b[1] - b[0]

                    b_press = ((target[0] * y) - (rest * a[0])) / (a[0] * x + y * b[0])
                    a_press = ((x * b_press) + rest) / y
                else:

                    a_press = ((target[0] * y) - (rest * b[0])) / (a[0] * y + x * b[0])
                    b_press = ((x * a_press) + rest) / y


                if int(a_press) == a_press and int(b_press) == b_press:
                    if is_part2:
                        part2 += int(a_press) * 3 + int(b_press)
                    else:
                        part1 += int(a_press) * 3 + int(b_press)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)
    

    # Old code used to solve part 1 using bfs
    def part1_bfs(self, machines):
        result = 0
        for machine in machines:
            # print(machine)

            queue = []
            lowest_cost = None
            vec_a = machine['a'][0] / machine['a'][1]
            vec_b = machine['b'][0] / machine['b'][1]
            visited = set()
            heapq.heappush(queue, (0, (0, 0), 0))
            while len(queue) > 0:
                cost, pos, button_presses = heapq.heappop(queue)

                if pos == machine['target']:
                    lowest_cost = cost
                    break

                if pos in visited:
                    continue
                visited.add(pos)

                if pos[0] >= machine['target'][0] or pos[1] >= machine['target'][1]:
                    continue

                # The vector of button A and button B make a cone.
                # The vector from the current position to the tatget needs to be in the cone for the target to be reachable
                vec_target = (machine['target'][0] - pos[0]) / (machine['target'][1] - pos[1])
                if not (min(vec_a, vec_b) <= vec_target <= max(vec_a, vec_b)):
                    continue

                for button in ['a', 'b']:
                    new_pos = (pos[0] + machine[button][0], pos[1] + machine[button][1])
                    new_cost = cost + (3 if button == 'a' else 1)
                    
                    heapq.heappush(queue, (new_cost, new_pos, button_presses + 1))

            if lowest_cost != None:
                result += lowest_cost
        return result


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
