from Table import Table
from time import time
from collections import deque

ORE = 'ore'
CLAY = 'clay'
OBSIDIAN = 'obsidian'
GEODE = 'geode'

RESOURCES = [ORE, CLAY, OBSIDIAN, GEODE]

class Robot:
    def __init__(self, type: str):
        self.type = type

class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Not Enough Minerals"
        self.input = self.getInput(self.day)

        self.blueprints = {}
        self.current_costs = {}

        self.calculated_scores = {}

    def load_blueprints(self):
        self.blueprints = {}
        for line in self.input.splitlines():
            blueprint, robots = line.split(': ')
            blueprint_id = int(blueprint.split(' ')[1])
            self.blueprints[blueprint_id] = {}

            for robot in robots.split('.')[:-1]:
                words = robot.split(' ')
                type = words[words.index('robot') - 1]
                self.blueprints[blueprint_id][type] = {}

                for resource in RESOURCES:
                    try:
                        resource_cost = int(words[words.index(resource, 2) - 1])
                        self.blueprints[blueprint_id][type][resource] = resource_cost
                    except:
                        self.blueprints[blueprint_id][type][resource] = 0

    def hash_dict(self, dictionary: dict):
        keys = sorted(dictionary.keys())
        return tuple([dictionary[key] for key in keys])

    def available_robots(self, resources: dict) -> list:
        available_robots = []
        for robot in RESOURCES:
            costs = self.current_costs[robot]
            can_construct = True
            for resource in RESOURCES:
                if costs[resource] > resources[resource]:
                    can_construct = False
                    break

            if can_construct:
                available_robots.append(robot)

        return available_robots

    def simulate(self, ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots, time_left: int):
        if time_left == 0:
            return geodes

        max_ore_cost = max([self.current_costs[robot][ORE] for robot in self.current_costs])
        max_clay_cost = max([self.current_costs[robot][CLAY] for robot in self.current_costs])
        max_obsidian_cost = max([self.current_costs[robot][OBSIDIAN] for robot in self.current_costs])

        # There is no point in having more robots than the max build cost of a resource for that robot
        if ore_robots >= max_ore_cost:
            ore_robots = max_ore_cost 
        if clay_robots >= max_clay_cost:
            clay_robots = max_clay_cost
        if obsidian_robots >= max_obsidian_cost:
            obsidian_robots = max_obsidian_cost

        # There is no point in stockpiling more resources than you can spend at max rate
        if ore >= (time_left * max_ore_cost) - (ore_robots * (time_left - 1)):
            ore = (time_left * max_ore_cost) - (ore_robots * (time_left - 1))
        if clay >= (time_left * max_clay_cost) - (clay_robots * (time_left - 1)):
            clay = (time_left * max_clay_cost) - (clay_robots * (time_left - 1))
        if obsidian >= (time_left * max_obsidian_cost) - (obsidian_robots * (time_left - 1)):
            obsidian = (time_left * max_obsidian_cost) - (obsidian_robots * (time_left - 1))

        state = (ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots, time_left)

        if state in self.calculated_scores:
            return self.calculated_scores[state]

        max_geodes = self.simulate(ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geodes + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots, time_left - 1)

        for robot in self.available_robots({ORE: ore, CLAY: clay, OBSIDIAN: obsidian, GEODE: geodes}):

            cost = self.current_costs[robot]

            max_geodes = max(max_geodes, self.simulate(
                ore + ore_robots - cost[ORE], clay + clay_robots - cost[CLAY], obsidian + obsidian_robots - cost[OBSIDIAN], geodes + geode_robots - cost[GEODE],
                ore_robots + (1 if robot == ORE else 0), clay_robots + (1 if robot == CLAY else 0), obsidian_robots + (1 if robot == OBSIDIAN else 0), geode_robots + (1 if robot == GEODE else 0), time_left - 1))

        self.calculated_scores[state] = max_geodes

        return max_geodes


    def solve(self):
        start_time = time()

        self.load_blueprints()

        self.printRow((self.day, self.title, '0 %', '', ''), end='\r')

        part1 = 0
        for blueprint in self.blueprints:
            self.current_costs = self.blueprints[blueprint]
            self.calculated_scores = {}

            max_geodes = self.simulate(
                0, 0, 0, 0, 
                1, 0, 0, 0,
                24
            )

            percentage = str(round(blueprint / len(self.blueprints.keys()) * 100, 1)) + ' %'
            self.printRow((self.day, self.title, percentage, '', ''), end='\r')

            part1 += (blueprint * max_geodes)

        self.printRow((self.day, self.title, part1, '0 %', ''), end='\r')
        
        part2 = 1
        for blueprint in [1, 2, 3]:
            self.current_costs = self.blueprints[blueprint]
            self.calculated_scores = {}

            max_geodes = self.simulate(
                0, 0, 0, 0, 
                1, 0, 0, 0,
                32
            )

            percentage = str(round(blueprint / 3 * 100, 1)) + ' %'
            self.printRow((self.day, self.title, part1, percentage, ''), end='\r')

            part2 = part2 * max_geodes

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
