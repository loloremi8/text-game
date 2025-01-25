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
        "Goblin": {"name": "Health Potion", "type": "consumable", "effect": {"health": 20}},
        "Orc": {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 5}},
        "Troll": {"name": "Troll Armor", "type": "armor", "effect": {"health": 30}},
        "Dragon": {"name": "Dragon Scale Shield", "type": "armor", "effect": {"health": 50}},
        "Lich": {"name": "Lich Staff", "type": "weapon", "effect": {"attack": 10}}
    }
    return loot_table.get(monster.name, None)