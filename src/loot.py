import random
from magic import fireball, heal, lightning, ice_blast, shield

def generate_loot(monster):
    """Generates loot based on the defeated monster."""
    loot_table = {
        "Goblin": [
            {"name": "Goblin Dagger", "type": "weapon", "effect": {"attack": 3}},
            {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}}
        ],
        "Orc": [
            {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 10}},
            {"name": "Orc Shield", "type": "armor", "effect": {"defense": 5}}
        ],
        "Troll": [
            {"name": "Troll Club", "type": "weapon", "effect": {"attack": 7}},
            {"name": "Troll Armor", "type": "armor", "effect": {"defense": 10}}
        ],
        "Dragon": [
            {"name": "Dragon Claw", "type": "weapon", "effect": {"attack": 15}},
            {"name": "Dragon Scale Shield", "type": "armor", "effect": {"defense": 10}}
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
        {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}},
        {"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}}
    ]
    loot_count = random.randint(1, 3)  # Generate between 1 and 3 loot items
    return random.sample(treasure_chest_loot, loot_count)

def generate_library_loot(player):
    """Generates random library loot."""
    known_spells = {spell.name for spell in player.spells}
    new_spells = get_new_spells(known_spells)

    library_loot = []

    if not known_spells:
        # Player knows no spells, give them the Heal spell, a mana potion and raise mana capacity
        library_loot.append(get_spell_book("Heal"))
        library_loot.append({"name": "Greater Mana Elixir", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 30}})
        library_loot.append({"name": "Greater Mana Potion", "type": "consumable_mana", "effect": {"mana": 30}})
    else:
        if new_spells:
            # Add a new spell book
            new_spell = random.choice(new_spells)
            library_loot.append(get_spell_book(new_spell.name))
        else:
            # No new spells to learn, add a mana potion
            library_loot.append({"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}})

    # Add additional loot items
    additional_loot = get_additional_loot()
    loot_count = random.randint(1, 2)  # Generate between 1 and 2 additional loot items
    additional_loot_sample = random.sample(additional_loot, loot_count)

    library_loot.extend(additional_loot_sample)
    return library_loot

def get_new_spells(known_spells):
    """Returns a list of new spells that the player does not know."""
    all_spells = [fireball, heal, lightning, ice_blast, shield]
    return [spell for spell in all_spells if spell.name not in known_spells]

def get_spell_book(spell_name):
    """Returns a spell book for the given spell name."""
    spell_books = {
        "Heal": {"name": "Grimmoire of Ancient magic", "type": "consumable_spell", "effect": {"spell": "Heal"}},
        "Fireball": {"name": "Pyromancer's Guide", "type": "consumable_spell", "effect": {"spell": "Fireball"}},
        "Lightning": {"name": "Stormbringer's Manual", "type": "consumable_spell", "effect": {"spell": "Lightning"}},
        "Ice Blast": {"name": "Frostbinder's Codex", "type": "consumable_spell", "effect": {"spell": "Ice Blast"}},
        "Shield": {"name": "Protector's Compendium", "type": "consumable_spell", "effect": {"spell": "Shield"}}
    }
    return spell_books[spell_name]

def get_additional_loot():
    """Returns a list of additional loot items."""
    return [
        {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 10}},
        {"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}},
        {"name": "Lesser Mana Elixir", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 15}},
        {"name": "Lesser Health Elixir", "type": "consumable_health_capacity", "effect": {"health_capacity": 15}}
    ]