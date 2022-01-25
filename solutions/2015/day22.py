from itertools import product
from Table import Table
from time import time

class NotEnoughManaException(Exception):
    pass
class SpellCastException(Exception):
    pass

class Player:
    def __init__(self, hp: int, damage: int, mana: int):
        self.hp = hp
        self.mana = mana
        self.damage = damage
        self.shield = 0
        self.poison = 0
        self.recharge = 0

    # when boss hits player
    def hit(self, damage: int):
        if self.shield > 0:
            armor = 7
        else:
            armor = 0

        damage_dealt = damage - armor

        if damage_dealt <= 0:
            damage_dealt = 1

        self.hp -= damage_dealt

    # when player casts a spell
    def cast(self, spell: dict):
        if self.mana < spell["cost"]:
            raise NotEnoughManaException("Not enough mana")

        self.mana -= spell["cost"]
        self.hp += spell["heal"]

        if spell["effect"] == "shield":
            if self.shield > 0:
                raise SpellCastException("You already have a shield")
            self.shield = spell["turns"]

        if spell["effect"] == "recharge":
            if self.recharge > 0:
                raise SpellCastException("You already being recharged")
            self.recharge = spell["turns"]


    # when boss receives spell effect
    def apply_effect(self, spell: dict):
        self.hp -= spell["damage"]

        if spell["effect"] == "poison":
            if self.poison > 0:
                raise SpellCastException("Boss is already poisoned")
            self.poison = spell["turns"]

    # at the start of each turn
    def effect(self):
        if self.shield > 0:
            self.shield -= 1

        if self.poison > 0:
            self.poison -= 1
            self.hp -= 3

        if self.recharge > 0:
            self.recharge -= 1
            self.mana += 101

    def is_defeated(self):
        return self.hp <= 0


class Day22(Table):

    def __init__(self):
        self.day = 22
        self.title = "Wizard Simulator 20XX"
        self.input = self.getInput(self.day)

        self.SPELLS = [
            { "name": "Magic Missile",  "cost": 53,   "damage": 4,  "heal": 0,  "effect": "",          "turns": 0 },
            { "name": "Drain",          "cost": 73,   "damage": 2,  "heal": 2,  "effect": "",          "turns": 0 },
            { "name": "Shield",         "cost": 113,  "damage": 0,  "heal": 0,  "effect": "shield",    "turns": 6 },
            { "name": "Poison",         "cost": 173,  "damage": 0,  "heal": 0,  "effect": "poison",    "turns": 6 },
            { "name": "Recharge",       "cost": 229,  "damage": 0,  "heal": 0,  "effect": "recharge",  "turns": 5 },
        ]

    def get_boss_stats(self):
        numbers = []
        for line in self.input.splitlines():
            number = int(line.split(":")[1].strip())
            numbers.append(number)

        return {
            "hp": numbers[0],
            "damage": numbers[1],
        }

    def play(self, player: Player, boss: Player, spells: list, hard: bool = False):
        try:
            for i, spell in enumerate(spells):
                if hard:
                    player.hit(1)

                player.effect()
                boss.effect()

                if player.is_defeated():
                    return 'boss', i - 1
                elif boss.is_defeated():
                    return 'player', i - 1

                player.cast(spell)
                boss.apply_effect(spell)

                if player.is_defeated():
                    return 'boss', i
                elif boss.is_defeated():
                    return 'player', i

                player.effect()
                boss.effect()

                if player.is_defeated():
                    return 'boss', i
                elif boss.is_defeated():
                    return 'player', i

                player.hit(boss.damage)

                if player.is_defeated():
                    return 'boss', i
                elif boss.is_defeated():
                    return 'player', i
        except NotEnoughManaException:
            return 'boss', i
        except SpellCastException:
            return 'neiter', i

        return 'neiter', i

    def solve(self):
        start_time = time()

        boss_stats = self.get_boss_stats()

        lowest_mana_win = 99999999999999999999999
        for spells in product(self.SPELLS, repeat=9):
            player = Player(50, 0, 500)
            boss = Player(boss_stats["hp"], boss_stats["damage"], 0)

            winner, spell_index = self.play(player, boss, spells)

            mana_cost = 0
            for i, spell in enumerate(spells):
                mana_cost += spell["cost"]

                if i == spell_index:
                    break

            if winner == "player" and mana_cost < lowest_mana_win:
                lowest_mana_win = mana_cost

        part1 = lowest_mana_win

        lowest_mana_win = 99999999999999999999999
        for spells in product(self.SPELLS, repeat=9):
            player = Player(50, 0, 500)
            boss = Player(boss_stats["hp"], boss_stats["damage"], 0)

            winner, spell_index = self.play(player, boss, spells, True)

            mana_cost = 0
            for i, spell in enumerate(spells):
                mana_cost += spell["cost"]

                if i == spell_index:
                    break

            if winner == "player" and mana_cost < lowest_mana_win:
                lowest_mana_win = mana_cost

        part2 = lowest_mana_win

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day22()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
