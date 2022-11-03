from Table import Table
from time import time
import re

TEAM_IMMUTE = 'immune_system'
TEAM_INFECTION = 'infection'

class Group:
    def __init__(self, id: int, team: str, units: int, hp: int, attack_type: str, attach_damage: int, initiative: int, immunities: tuple, weaknesses: tuple):
        self.id = id
        self.team = team
        self.units = units
        self.hp = hp
        self.attack_type = attack_type
        self.attack_damage = attach_damage
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses

        self.target = None

    def effective_power(self):
        return self.units * self.attack_damage

    def possible_damage(self, target_group):
        damage = self.effective_power()
        if self.attack_type in target_group.immunities:
            damage = 0
        elif self.attack_type in target_group.weaknesses:
            damage *= 2

        return damage

    def set_target(self, target_group):
        self.target = target_group

    def attack_target(self):
        if self.target is None:
            return
        if self.units <= 0:
            return

        damage = self.possible_damage(self.target)
        killed_units = damage // self.target.hp
        self.target.units -= killed_units

        # print('group ' + str(self.id) + ' does ' + str(damage) + ' damage to group ' + str(self.target.id) + ', killing ' + str(killed_units) + ' units. units left: ' + str(self.target.units))
        return killed_units > 0


class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Immune System Simulator 20XX"
        self.input = self.getInput(self.day)

        self.groups = []

    def load_groups(self, boost = 0):
        self.groups = []
        team = None
        id = 1
        for line in self.input.splitlines():
            results = re.search("^(?P<units>\d+) units each with (?P<hp>\d+) hit points( \((?P<abilities>[a-z ,;]+)\))? with an attack that does (?P<attack_damage>\d+) (?P<attack_type>\w+) damage at initiative (?P<initiative>\d+)$", line)
            
            if results is None and team is None:
                team = TEAM_IMMUTE
                continue
            elif results is None:
                team = TEAM_INFECTION
                boost = 0
                continue

            props = results.groupdict()
            immunities = ()
            weaknesses = ()

            if props['abilities'] is not None:
                immune_results = re.search("immune to ([\w, ]*)", props['abilities'])
                weakness_results = re.search("weak to ([\w, ]*)", props['abilities'])

                if immune_results is not None:
                    immunities = tuple(immune_results.groups()[0].split(', '))
                
                if weakness_results is not None:
                    weaknesses = tuple(weakness_results.groups()[0].split(', '))

            self.groups.append(Group(
                id,
                team, 
                int(props['units']), 
                int(props['hp']), 
                props['attack_type'], 
                int(props['attack_damage']) + boost, 
                int(props['initiative']), 
                immunities, 
                weaknesses
            ))

            id += 1

    def fight(self):
        # target selection phase
        ordered_groups = sorted(self.groups, key=lambda group: (group.effective_power(), group.initiative), reverse=True)
        targeted_groups = []
        for group in ordered_groups:
            possible_targets = [possible_group for possible_group in self.groups if possible_group.id not in targeted_groups and possible_group.team != group.team]
            ranked_targets = sorted(possible_targets, key=lambda target_group: (group.possible_damage(target_group), target_group.effective_power(), target_group.initiative), reverse=True)
            
            if len(ranked_targets) > 0 and group.possible_damage(ranked_targets[0]) > 0:
                target = ranked_targets[0]
                group.set_target(target)
                targeted_groups.append(target.id)
            else:
                group.set_target(None)

        # attacking phase
        killed_any_units = False
        ordered_groups = sorted(self.groups, key=lambda group: group.initiative, reverse=True)
        for group in ordered_groups:
            killed_units = group.attack_target()
            if not killed_any_units and killed_units:
                killed_any_units = True

        return killed_any_units

    def battle(self):
        killed_units = True
        while len(set([group.team for group in self.groups])) > 1 and killed_units:
            killed_units = self.fight()

            # remove dead groups
            self.groups = [group for group in self.groups if group.units > 0]

    def solve(self):
        start_time = time()

        self.load_groups()
        self.battle()
        part1 = sum(group.units for group in self.groups)

        boost = 1
        while True:
            self.load_groups(boost)
            self.battle()

            won = len(set([group.team for group in self.groups])) == 1 and self.groups[0].team == TEAM_IMMUTE

            if won:
                break

            boost += 1
        
        part2 = sum(group.units for group in self.groups)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
