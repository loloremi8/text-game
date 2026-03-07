import random


class Monster:
    def __init__(self, name, health, attack, defense, difficulty):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.difficulty = difficulty

    def display_status(self):
        """Displays the monster's status."""
        stats = f"""Monster Stats:
--------------
Name: {self.name}
Health: {self.health}/{self.max_health}
Attack: {self.attack}
Defense: {self.defense}
Difficulty: {self.difficulty}"""
        return stats

    def clone(self):
        """Returns a new monster with the same base stats."""
        return Monster(self.name, self.max_health, self.attack, self.defense, self.difficulty)


def generate_loot(monster):
    """Generates loot based on the defeated monster."""
    loot_table = {
        "Goblin": [
            {"name": "Goblin Dagger", "type": "weapon", "effect": {"attack": 3}, "rarity": "common"},
            {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"}
        ],
        "Skeleton": [
            {"name": "Bone Club", "type": "weapon", "effect": {"attack": 4}, "rarity": "common"},
            {"name": "Bone Shield", "type": "armor", "slot": "shield", "effect": {"defense": 2}, "rarity": "common"}
        ],
        "Orc": [
            {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 6}, "rarity": "uncommon"},
            {"name": "Orc Shield", "type": "armor", "slot": "shield", "effect": {"defense": 2}, "rarity": "uncommon"}
        ],
        "Zombie": [
            {"name": "Rotten Club", "type": "weapon", "effect": {"attack": 7}, "rarity": "uncommon"},
            {"name": "Tattered Armor", "type": "armor", "slot": "chestplate", "effect": {"defense": 3}, "rarity": "uncommon"}
        ],
        "Troll": [
            {"name": "Troll Club", "type": "weapon", "effect": {"attack": 9}, "rarity": "rare"},
            {"name": "Troll Armor", "type": "armor", "slot": "chestplate", "effect": {"defense": 4}, "rarity": "rare"}
        ],
        "Vampire": [
            {"name": "Vampire Fang", "type": "weapon", "effect": {"attack": 11}, "rarity": "rare"},
            {"name": "Vampire Cloak", "type": "armor", "slot": "chestplate", "effect": {"defense": 5}, "rarity": "rare"}
        ],
        "Dark Knight": [
            {"name": "Knight's Blade", "type": "weapon", "effect": {"attack": 10}, "rarity": "rare"},
            {"name": "Knight's Armor", "type": "armor", "slot": "chestplate", "effect": {"defense": 4}, "rarity": "rare"},
            {"name": "Greater Health Potion", "type": "consumable_health", "effect": {"health": 40}, "rarity": "rare"}
        ],
        "Lich": [
            {"name": "Lich Staff", "type": "weapon", "effect": {"attack": 14}, "rarity": "legendary"},
            {"name": "Lich Robe", "type": "armor", "slot": "chestplate", "effect": {"defense": 5}, "rarity": "legendary"}
        ],
        "Dragon": [
            {"name": "Dragon Claw", "type": "weapon", "effect": {"attack": 18}, "rarity": "epic"},
            {"name": "Dragon Scale Shield", "type": "armor", "slot": "shield", "effect": {"defense": 7}, "rarity": "epic"},
            {"name": "Dragon's Heart", "type": "consumable_health", "effect": {"health": 50}, "rarity": "legendary"},
            {"name": "Dragon's Vitality", "type": "consumable_health_capacity", "effect": {"health_capacity": 25}, "rarity": "legendary"}
        ],
        "Demon Lord": [
            {"name": "Demon Sword", "type": "weapon", "effect": {"attack": 22}, "rarity": "legendary"},
            {"name": "Demon Armor", "type": "armor", "slot": "chestplate", "effect": {"defense": 10}, "rarity": "legendary"}
        ]
    }

    monster_loot = loot_table.get(monster.name, [])
    if not monster_loot:
        return []

    # Dragon and bosses drop 2-3 items, regular monsters drop 0-1
    if monster.difficulty == "boss":
        num_drops = random.randint(2, 3)
    else:
        num_drops = random.randint(0, 1)

    return random.sample(monster_loot, min(num_drops, len(monster_loot)))


# Create actual monster instances
Goblin = Monster("Goblin", 25, 5, 1, "easy")
Skeleton = Monster("Skeleton", 35, 10, 3, "easy")
Orc = Monster("Orc", 45, 14, 3, "medium")
Zombie = Monster("Zombie", 50, 12, 2, "medium")
Troll = Monster("Troll", 70, 18, 4, "hard")
Vampire = Monster("Vampire", 65, 20, 3, "hard")
DarkKnight = Monster("Dark Knight", 100, 25, 5, "boss")
Lich = Monster("Lich", 110, 25, 4, "boss")
Dragon = Monster("Dragon", 180, 35, 5, "boss")
DemonLord = Monster("Demon Lord", 220, 40, 6, "boss")

# List of normal monsters
normal_monsters = [Goblin, Skeleton, Orc, Zombie, Troll, Vampire]

# List of special monsters
special_monsters = [Lich, DarkKnight]

boss_monsters = [Dragon, DemonLord]