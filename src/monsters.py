class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def display_status(self):
        """Displays the monster's status."""
        stats = f"""
        Monster Stats:
        --------------
        Name: {self.name}
        Health: {self.health}
        Attack: {self.attack}
        """
        return stats
    
# List of normal monsters
normal_monsters = [
    Monster("Goblin", 30, 5),
    Monster("Orc", 50, 10),
    Monster("Troll", 80, 15)
]

# List of special monsters
special_monsters = [
    Monster("Dragon", 200, 25),
    Monster("Lich", 150, 20)
]

def generate_loot(monster):
    """Generates loot based on the defeated monster."""
    loot_table = {
        "Goblin": [
            {"name": "Health Potion", "type": "consumable", "effect": {"health": 20}},
            {"name": "Goblin Dagger", "type": "weapon", "effect": {"attack": 3}}
        ],
        "Orc": [
            {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 5}},
            {"name": "Orc Shield", "type": "armor", "effect": {"defense": 2}}
        ],
        "Troll": [
            {"name": "Troll Armor", "type": "armor", "effect": {"defense": 5}},
            {"name": "Troll Club", "type": "weapon", "effect": {"attack": 7}}
        ],
        "Dragon": [
            {"name": "Dragon Scale Shield", "type": "armor", "effect": {"defense": 10}},
            {"name": "Dragon Claw", "type": "weapon", "effect": {"attack": 15}}
        ],
        "Lich": [
            {"name": "Lich Staff", "type": "weapon", "effect": {"attack": 10}},
            {"name": "Lich Robe", "type": "armor", "effect": {"defense": 5}}
        ]
    }
    return loot_table.get(monster.name, [])