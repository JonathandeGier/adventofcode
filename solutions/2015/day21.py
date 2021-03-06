from Table import Table
from time import time

class Player:
    def __init__(self, hp: int, damage: int, armor: int):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def hit(self, damage: int):
        damage_dealt = damage - self.armor
        if damage_dealt <= 0:
            damage_dealt = 1
        self.hp -= damage_dealt

    def is_defeated(self):
        return self.hp <= 0

class Day21(Table):

    def __init__(self):
        self.day = 21
        self.title = "RPG Simulator 20XX"
        self.input = self.getInput(self.day)

        self.WEAPONS = (
            { "name": "Dagger",      "cost": 8,   "damage": 4, "armor": 0 },
            { "name": "Shortsword",  "cost": 10,  "damage": 5, "armor": 0 },
            { "name": "Warhammer",   "cost": 25,  "damage": 6, "armor": 0 },
            { "name": "Longsword",   "cost": 40,  "damage": 7, "armor": 0 },
            { "name": "GreatAxe",    "cost": 74,  "damage": 8, "armor": 0 }
        )

        self.ARMOR = (
            { "name": "No armor",    "cost": 0,   "damage": 0, "armor": 0 },
            { "name": "Leather",     "cost": 13,  "damage": 0, "armor": 1 },
            { "name": "Chainmail",   "cost": 31,  "damage": 0, "armor": 2 },
            { "name": "Splintmail",  "cost": 53,  "damage": 0, "armor": 3 },
            { "name": "Bandedmail",  "cost": 75,  "damage": 0, "armor": 4 },
            { "name": "Platemail",   "cost": 102, "damage": 0, "armor": 5 },
        )

        self.RINGS = (
            { "name": "No ring (L)", "cost": 0,   "damage": 0, "armor": 0 },
            { "name": "No ring (R)", "cost": 0,   "damage": 0, "armor": 0 },
            { "name": "Damage +1",   "cost": 25,  "damage": 1, "armor": 0 },
            { "name": "Damage +2",   "cost": 50,  "damage": 2, "armor": 0 },
            { "name": "Damage +3",   "cost": 100, "damage": 3, "armor": 0 },
            { "name": "Defence +1",  "cost": 20,  "damage": 0, "armor": 1 },
            { "name": "Defence +2",  "cost": 40,  "damage": 0, "armor": 2 },
            { "name": "Defence +3",  "cost": 80,  "damage": 0, "armor": 3 },
        )

    def get_boss_stats(self):
        numbers = []
        for line in self.input.splitlines():
            number = int(line.split(":")[1].strip())
            numbers.append(number)

        return {
            "hp": numbers[0],
            "damage": numbers[1],
            "armor": numbers[2],
        }

    def equipment_combinations(self):
        for weapon in self.WEAPONS:
            for armor in self.ARMOR:
                for ring1 in self.RINGS:
                    for ring2 in self.RINGS:
                        if ring1["name"] == ring2["name"]:
                            continue
                        yield [weapon, armor, ring1, ring2]

    def play(self, player: Player, boss: Player):
        while True:
            boss.hit(player.damage)
            if boss.is_defeated():
                return "player"
            
            player.hit(boss.damage)
            if player.is_defeated():
                return "boss"

    def solve(self):
        start_time = time()

        boss_stats = self.get_boss_stats()

        lowest_cost_win = 356 # cost of most expensive items
        for combination in self.equipment_combinations():
            cost = 0
            damage = 0
            armor = 0

            for equipment in combination:
                cost += equipment["cost"]
                damage += equipment["damage"]
                armor += equipment["armor"]

            player = Player(100, damage, armor)
            boss = Player(boss_stats["hp"], boss_stats["damage"], boss_stats["armor"])

            winner = self.play(player, boss)
            if winner == "player" and cost < lowest_cost_win:
                lowest_cost_win = cost

        part1 = lowest_cost_win

        highest_cost_lose = 0
        for combination in self.equipment_combinations():
            cost = 0
            damage = 0
            armor = 0

            for equipment in combination:
                cost += equipment["cost"]
                damage += equipment["damage"]
                armor += equipment["armor"]

            player = Player(100, damage, armor)
            boss = Player(boss_stats["hp"], boss_stats["damage"], boss_stats["armor"])

            winner = self.play(player, boss)
            if winner == "boss" and cost > highest_cost_lose:
                highest_cost_lose = cost

        part2 = highest_cost_lose

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day21()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
