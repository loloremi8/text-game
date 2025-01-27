import random
from magic import fireball, heal, lightning, ice_blast, shield

def generate_loot(monster):
    """Generates loot based on the defeated monster."""
    loot_table = {
        "Goblin": [
            {"name": "Health Potion", "type": "consumable_health", "effect": {"health": 20}},
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

def generate_treasure_chest_loot():
    """Generates random treasure chest loot."""
    treasure_chest_loot = [
        {"name": "Rusty Sword", "type": "weapon", "effect": {"attack": 5}},
        {"name": "Health Potion", "type": "consumable_health", "effect": {"health": 20}},
        {"name": "Mana Potion", "type": "consumable_mana", "effect": {"mana": 20}}
    ]
    loot_count = random.randint(1, 3)  # Generate between 1 and 3 loot items
    return random.sample(treasure_chest_loot, loot_count)

def generate_library_loot(player):
    """Generates random library loot."""
    known_spells = {spell.name for spell in player.spells}
    all_spells = [fireball, heal, lightning, ice_blast, shield]
    new_spells = [spell for spell in all_spells if spell.name not in known_spells]

    spell_books = {
        "Fireball": {"name": "Pyromancer's Guide", "type": "consumable_spell", "effect": {"spell": "Fireball"}},
        "Heal": {"name": "Ancient Tome of Healing", "type": "consumable_spell", "effect": {"spell": "Heal"}},
        "Lightning": {"name": "Stormbringer's Manual", "type": "consumable_spell", "effect": {"spell": "Lightning"}},
        "Ice Blast": {"name": "Frostbinder's Codex", "type": "consumable_spell", "effect": {"spell": "Ice Blast"}},
        "Shield": {"name": "Protector's Compendium", "type": "consumable_spell", "effect": {"spell": "Shield"}}
    }

    library_loot = []

    if not known_spells:
        # Player knows no spells, give them the Heal spell and raise mana capacity
        library_loot.append(spell_books["Heal"])
        player.max_mana = max(player.max_mana, 20)
        player.mana = max(player.mana, 20)
        library_loot.append({"name": "Mana Capacity Increase", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 20}})
    else:
        if new_spells:
            # Add a new spell book
            new_spell = random.choice(new_spells)
            library_loot.append(spell_books[new_spell.name])
        else:
            # No new spells to learn, add a mana potion
            library_loot.append({"name": "Mana Potion", "type": "consumable_mana", "effect": {"mana": 20}})

    # Add additional loot items
    additional_loot = [
        {"name": "Health Potion", "type": "consumable_health", "effect": {"health": 20}},
        {"name": "Mana Potion", "type": "consumable_mana", "effect": {"mana": 20}},
        {"name": "Mana Elixir", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 10}},
        {"name": "Health Elixir", "type": "consumable_health_capacity", "effect": {"health_capacity": 20}}
    ]
    loot_count = random.randint(1, 2)  # Generate between 1 and 2 additional loot items
    library_loot.extend(random.sample(additional_loot, loot_count))

    return library_loot