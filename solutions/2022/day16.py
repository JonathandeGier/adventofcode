from Table import Table
from time import time
import heapq

FOUND_SCORES = {}

class Valve:
    def __init__(self, name: str, flow: int, tunnels: list):
        self.name = name
        self.flow = flow
        self.tunnels = tunnels

class Day16(Table):

    def __init__(self):
        self.day = 16
        self.title = "Proboscidea Volcanium"
        self.input = self.getInput(self.day)

        self.valves = {}
        self.valves_of_interest = []
        self.travel_cost = {}

    def load_valves(self):
        self.valves = {}
        for line in self.input.splitlines():
            words = line.split(' ')
            name = words[1]
            flow = int(words[4].split('=')[1][:-1])
            tunnels = [val[:2] for val in words[9:]]
            
            self.valves[name] = Valve(name, flow, tunnels)

        # The majority of valves dont have flow
        # So to reduce the search space only consider the valves that actually flow once opened
        self.valves_of_interest = [valve.name for valve in self.valves.values() if valve.flow > 0]
        
        # Also claculate the travel cost to go from any valve with flow (+ starting valve) to any other valve with flow
        self.travel_cost = {}
        for start_valve in self.valves_of_interest + ['AA']:
            self.travel_cost[start_valve] = {}
            for end_valve in self.valves_of_interest:
                if start_valve == end_valve:
                    continue

                self.travel_cost[start_valve][end_valve] = self.calculate_travel_cost(start_valve, end_valve)

    # calculates the shortest travel time between any two valves
    def calculate_travel_cost(self, start: str, end: str):
        queue = []
        heapq.heappush(queue, (0, start))
        while len(queue) > 0:
            time_spent, current_valve = heapq.heappop(queue)
            if current_valve == end:
                return time_spent

            valve = self.valves[current_valve]
            for other_valve in valve.tunnels:
                heapq.heappush(queue, (time_spent + 1, other_valve))

    def find_score(self, current_valve: str, opened_valves: set, time_left: int, other_palyers: int):
        # If you are out of time, you can only get a max score of 0
        if time_left <= 0:
            # if another player still has to go through (elephant), return that score
            if other_palyers > 0:
                # (start at AA, it cannot open valves that are already opened by the other player, same 26 minutes, one less player)
                return self.find_score('AA', opened_valves, 26, other_palyers - 1)
            return 0

        # game states can occur multiple times, and the same game state will produce the same score
        # So we return the score from a "cache" if it has already been calculated 
        state = (current_valve, frozenset(opened_valves), time_left, other_palyers)
        if state in FOUND_SCORES:
            return FOUND_SCORES[state]

        # Claculate the actual score for this game state
        score = 0
        valve = self.valves[current_valve]

        # we can only open a valve if it is not already opened, and we should not open valves that dont flow (since that will only cost time)
        if current_valve not in opened_valves and valve.flow > 0:
            new_opened_valves = opened_valves.copy()
            new_opened_valves.add(current_valve)
            score = max(score, (time_left - 1) * valve.flow + self.find_score(current_valve, new_opened_valves, time_left - 1, other_palyers))
        
        # Move to the next interesting valve
        for next_valve in self.valves_of_interest:
            # not the current valve
            if next_valve == current_valve: 
                continue

            # not an already opened valve
            if next_valve in opened_valves: 
                continue

            # Notice this score may be higher than the score if we opened the current valve
            # That way the other player (elephant) can also open some valves
            score = max(score, self.find_score(next_valve, opened_valves, time_left - self.travel_cost[current_valve][next_valve], other_palyers))

        # Store and return the calculated score
        FOUND_SCORES[state] = score

        return score

    def solve(self):
        start_time = time()

        self.load_valves()

        # part 1 (origional solution)
        queue = []
        max_pressure = 0
        heapq.heappush(queue, (0, 0, 0, 30, 'AA', set()))
        while len(queue) > 0:
            _, _, pressure, time_left, current_valve, visited = heapq.heappop(queue)

            visited.add(current_valve)

            if self.valves[current_valve].flow > 0:
                time_left -= 1

            pressure += (self.valves[current_valve].flow * time_left)

            possible_valves = [valve for valve in self.valves_of_interest if valve not in visited]
            
            if len(possible_valves) == 0:
                # end of scenario: all valves of interest are open with time to spare
                max_pressure = max(max_pressure, pressure)

            for next_valve in possible_valves:
                new_time_left = time_left - self.travel_cost[current_valve][next_valve]
                if new_time_left > 1:
                    heapq.heappush(queue, (-pressure, -time_left, pressure, time_left - self.travel_cost[current_valve][next_valve], next_valve, visited.copy()))
                else:
                    # end of scenario: no time left to open any other valve
                    max_pressure = max(max_pressure, pressure)

        part1 = max_pressure
        self.printRow((self.day, self.title, part1, 'Be patient ...', ''), end='\r')

        part2 = self.find_score('AA', set(), 26, 1)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day16()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
