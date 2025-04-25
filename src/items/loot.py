import random
from combat.magic import fireball, heal, lightning, ice_blast, shield

RARITY_LEVELS = ["common", "uncommon", "rare", "epic", "legendary"]

def generate_treasure_chest_loot():
    """Generates random treasure chest loot."""
    treasure_chest_loot = [
        {"name": "Rusty Sword", "type": "weapon", "effect": {"attack": 5}, "rarity": "common"},
        {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"},
        {"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}, "rarity": "common"}
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
        library_loot.append({"name": "Greater Mana Elixir", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 30}, "rarity": "rare"})
        library_loot.append({"name": "Greater Mana Potion", "type": "consumable_mana", "effect": {"mana": 30}, "rarity": "rare"})
    else:
        if new_spells:
            # Add a new spell book
            new_spell = random.choice(new_spells)
            library_loot.append(get_spell_book(new_spell.name))
        else:
            # No new spells to learn, add a mana potion
            library_loot.append({"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}, "rarity": "common"})

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
        "Heal": {"name": "Grimmoire of Ancient magic", "type": "consumable_spell", "effect": {"spell": "Heal"}, "rarity": "common"},
        "Fireball": {"name": "Pyromancer's Guide", "type": "consumable_spell", "effect": {"spell": "Fireball"}, "rarity": "common"},
        "Lightning": {"name": "Stormbringer's Manual", "type": "consumable_spell", "effect": {"spell": "Lightning"}, "rarity": "uncommon"},
        "Ice Blast": {"name": "Frostbinder's Codex", "type": "consumable_spell", "effect": {"spell": "Ice Blast"}, "rarity": "rare"},
        "Shield": {"name": "Protector's Compendium", "type": "consumable_spell", "effect": {"spell": "Shield"}, "rarity": "common"}
    }
    return spell_books[spell_name]

def get_additional_loot():
    """Returns a list of additional loot items."""
    return [
        {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 10}, "rarity": "common"},
        {"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}, "rarity": "common"},
        {"name": "Lesser Mana Elixir", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 15}, "rarity": "uncommon"},
        {"name": "Lesser Health Elixir", "type": "consumable_health_capacity", "effect": {"health_capacity": 15}, "rarity": "uncommon"}
    ]

def get_kitchen_loot():
    """Returns a list of kitchen loot items."""
    kitech_loot = [
        {"name": "Apple", "type": "consumable_health", "effect": {"health": 5}, "rarity": "common"},
        {"name": "Bread", "type": "consumable_health", "effect": {"health": 10}, "rarity": "common"},
        {"name": "Wine", "type": "consumable_mana", "effect": {"mana": 10}, "rarity": "common"},
        {"name": "Cheese", "type": "consumable_health", "effect": {"health": 10}, "rarity": "common"}
    ]
    loot_count = random.randint(2, 3)   # Generate between 2 and 3 loot items
    return random.sample(kitech_loot, loot_count)

def get_dining_hall_loot():
    """Returns a list of dining hall loot items."""
    dining_hall_loot = [
        {"name": "Roast Chicken", "type": "consumable_health", "effect": {"health": 20}, "rarity": "uncommon"},
        {"name": "Goblet of Wine", "type": "consumable_mana", "effect": {"mana": 20}, "rarity": "uncommon"},
        {"name": "Fruit Platter", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"},
        {"name": "Cheese Platter", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"}
    ]
    loot_count = random.randint(2, 3)  # Generate between 2 and 3 loot items
    return random.sample(dining_hall_loot, loot_count)

def get_garden_loot():
    """Returns a list of garden loot items."""
    garden_loot = [
        {"name": "Healing Herb", "type": "consumable_health", "effect": {"health": 10}, "rarity": "common"},
        {"name": "Mana Herb", "type": "consumable_mana", "effect": {"mana": 10}, "rarity": "common"},
        {"name": "Rare Flower", "type": "consumable_health", "effect": {"health": 20}, "rarity": "uncommon"},
        {"name": "Mystic Herb", "type": "consumable_mana", "effect": {"mana": 20}, "rarity": "uncommon"}
    ]
    loot_count = random.randint(2, 3)  # Generate between 2 and 3 loot items
    return random.sample(garden_loot, loot_count)