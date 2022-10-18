from collections import deque
from Table import Table
from time import time
import sys

ELF = 'E'
GOBLIN = 'G'

EMPTY = '.'
WALL = '#'

class Unit:
    def __init__(self, id: int, type: str, position: tuple, damage: int):
        self.id = id
        self.type = type
        self.position = position

        self.hp = 200
        self.damage = damage

        self.dead = False

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Beverage Bandits"
        self.input = self.getInput(self.day)

        self.map = None
        self.units = None

    def load_data(self, elf_damage = 3):
        map = [[*line] for line in self.input.splitlines()]
        
        self.map = {}
        self.units = []

        # x is the vertical axis, y is the horizontal axis
        # this way sorting a array of positions will put them in reading order
        id = 1
        for x, line in enumerate(map):
            for y, char in enumerate(line):
                self.map[(x, y)] = char
                if char in [ELF, GOBLIN]:
                    damage = 3
                    if char == ELF:
                        damage = elf_damage
                    self.units.append(Unit(id, char, (x, y), damage))
                    self.map[(x, y)] = EMPTY

                    id += 1

    def adjacent(self, location: tuple, ignore_units = False):
        result = []
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (location[0] + direction[0], location[1] + direction[1])
            if self.map[new_pos] == EMPTY and (ignore_units or len([unit for unit in self.units if unit.position == new_pos and not unit.dead]) == 0):
                result.append(new_pos)
        return result


    def distance_fill(self, location: tuple):
        distances = {}
        distances[location] = 0

        queue = deque()
        queue.append(location)

        while len(queue) > 0:
            loc = queue.popleft()
            distance = distances[loc] + 1

            for adjacent in self.adjacent(loc):
                if adjacent in distances:
                    continue

                distances[adjacent] = distance
                queue.append(adjacent)

        return distances


    def move(self, unit: Unit):
        if unit.dead:
            return

        enemies = [u for u in self.units if u.type != unit.type and not u.dead]

        adjacent_locations = self.adjacent(unit.position)
        
        # do not move if an enemy is in range
        enemy_in_range = False
        for adjacent_location in self.adjacent(unit.position, True):
            if len([enemy for enemy in enemies if enemy.position == adjacent_location]) > 0:
                enemy_in_range = True
                break

        if enemy_in_range:
            return

        # get all locations where the unit is in range of an enemy
        in_range = set()
        for enemy in enemies:
            for location in self.adjacent(enemy.position):
                in_range.add(location)

        # calculate wich of those locations are reachable
        reachable = {}
        for location in in_range:
            distances = self.distance_fill(location)

            for adjacent_location in adjacent_locations:
                if adjacent_location in distances:
                    reachable[location] = distances

        # if no enemy is reachable, do not move
        if len(reachable.keys()) == 0:
            return

        # get the closest location
        closest = min([min([distances[adjacent_location] if adjacent_location in distances else sys.maxsize for distances in reachable.values()]) for adjacent_location in adjacent_locations])
        nearest = {}
        for location in reachable:
            distances = reachable[location]

            for adjacent_location in adjacent_locations:
                if adjacent_location in distances and distances[adjacent_location] == closest:
                    nearest[location] = distances

        chosen_target_location = sorted(nearest.keys())[0]

        viable_new_locations = []
        for adjacent_location in adjacent_locations:
            if adjacent_location in nearest[chosen_target_location] and nearest[chosen_target_location][adjacent_location] == closest:
                viable_new_locations.append(adjacent_location)
        
        new_position = sorted(viable_new_locations)[0]

        unit.position = new_position

    def attack(self, unit: Unit):
        if unit.dead:
            return

        all_adjacent_locations = self.adjacent(unit.position, True)
        enemies_in_range = [enemy for enemy in self.units if enemy.type != unit.type and enemy.position in all_adjacent_locations and not enemy.dead]

        if len(enemies_in_range) == 0:
            return

        lowest_hp = min([enemy.hp for enemy in enemies_in_range])
        lowest_enemies = [enemy for enemy in enemies_in_range if enemy.hp == lowest_hp]

        first_in_order = sorted([enemy.position for enemy in lowest_enemies])[0]
        target_enemy = [enemy for enemy in lowest_enemies if enemy.position == first_in_order][0]

        target_enemy.hp -= unit.damage
        if target_enemy.hp <= 0:
            target_enemy.dead = True


    def round(self):
        sorted_units = sorted(self.units, key=lambda x: x.position)

        for unit in sorted_units:
            self.move(unit)
            self.attack(unit)

    def battle(self, do_print = True):
        rounds = 0
        while True:
            if do_print:
                self.printRow((self.day, self.title, 'round ' + str(rounds + 1), '', ''), end="\r")

            no_elfs = len([unit for unit in self.units if unit.type == ELF and not unit.dead])
            no_goblins = len([unit for unit in self.units if unit.type == GOBLIN and not unit.dead])

            if no_elfs == 0 or no_goblins == 0:
                break
            
            self.round()
            rounds += 1

        return (rounds - 1) * sum([unit.hp for unit in self.units if not unit.dead])


    def solve(self):
        start_time = time()

        self.load_data()

        part1 = self.battle()

        # start relatively high to check less scenario's
        damage = 20
        elfs = len([unit for unit in self.units if unit.type == ELF])
        while True:
            self.printRow((self.day, self.title, part1, 'attempting ' + str(damage), ''), end="\r")
            self.load_data(damage)
            part2 = self.battle(False)

            if len([unit for unit in self.units if unit.type == ELF and not unit.dead]) == elfs:
                break

            damage += 1

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
