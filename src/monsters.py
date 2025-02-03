class Monster:
    def __init__(self, name, health, attack, difficulty):
        self.name = name
        self.health = health
        self.attack = attack
        self.difficulty = difficulty

    def display_status(self):
        """Displays the monster's status."""
        stats = f"""
        Monster Stats:
        --------------
        Name: {self.name}
        Health: {self.health}
        Attack: {self.attack}
        Difficulty: {self.difficulty}
        """
        return stats

def generate_loot(monster):
    """Generates loot based on the defeated monster."""
    loot_table = {
        "Goblin": [
            {"name": "Goblin Dagger", "type": "weapon", "effect": {"attack": 3}, "rarity": "common"},
            {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"}
        ],
        "Skeleton": [
            {"name": "Bone Club", "type": "weapon", "effect": {"attack": 5}, "rarity": "common"},
            {"name": "Bone Shield", "type": "armor", "effect": {"defense": 3}, "rarity": "common"}
        ],
        "Orc": [
            {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 8}, "rarity": "uncommon"},
            {"name": "Orc Shield", "type": "armor", "effect": {"defense": 4}, "rarity": "uncommon"}
        ],
        "Zombie": [
            {"name": "Rotten Club", "type": "weapon", "effect": {"attack": 10}, "rarity": "uncommon"},
            {"name": "Tattered Armor", "type": "armor", "effect": {"defense": 5}, "rarity": "uncommon"}
        ],
        "Troll": [
            {"name": "Troll Club", "type": "weapon", "effect": {"attack": 15}, "rarity": "rare"},
            {"name": "Troll Armor", "type": "armor", "effect": {"defense": 8}, "rarity": "rare"}
        ],
        "Vampire": [
            {"name": "Vampire Fang", "type": "weapon", "effect": {"attack": 18}, "rarity": "rare"},
            {"name": "Vampire Cloak", "type": "armor", "effect": {"defense": 10}, "rarity": "rare"}
        ],
        "Lich": [
            {"name": "Lich Staff", "type": "weapon", "effect": {"attack": 20}, "rarity": "legendary"},
            {"name": "Lich Robe", "type": "armor", "effect": {"defense": 10}, "rarity": "legendary"}
        ],
        "Dragon": [
            {"name": "Dragon Claw", "type": "weapon", "effect": {"attack": 25}, "rarity": "epic"},
            {"name": "Dragon Scale Shield", "type": "armor", "effect": {"defense": 15}, "rarity": "epic"}
        ],
        "Demon Lord": [
            {"name": "Demon Sword", "type": "weapon", "effect": {"attack": 30}, "rarity": "legendary"},
            {"name": "Demon Armor", "type": "armor", "effect": {"defense": 20}, "rarity": "legendary"}
        ]
    }
    return loot_table.get(monster.name, [])

# List of normal monsters
normal_monsters = [
    # Easy monsters
    Monster("Goblin", 30, 5, "easy"),
    Monster("Skeleton", 40, 7, "easy"),
    # Medium monsters
    Monster("Orc", 50, 10, "medium"),
    Monster("Zombie", 60, 12, "medium"),
    # Hard monsters
    Monster("Troll", 80, 15, "hard"),
    Monster("Vampire", 90, 18, "hard")
]

# List of special monsters
special_monsters = [
    Monster("Lich", 150, 20, "boss"),
    Monster("Dragon", 200, 25, "boss"),
    Monster("Demon Lord", 250, 30, "boss")
]