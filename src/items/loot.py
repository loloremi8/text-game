import random
from combat.magic import fireball, heal, lightning, ice_blast, shield

RARITY_LEVELS = ["common", "uncommon", "rare", "epic", "legendary"]

def get_library_loot(player):
    """Generates random library loot.
    
    - If player doesn't have heal: guaranteed heal book + mana crystal + mana potion + small chance at a second spell
    - If player already has heal: just a chance at a new spell + additional loot
    """
    known_spell_names = {spell.name.lower() for spell in player.spells}
    library_loot = []

    if "heal" not in known_spell_names:
        # Player doesn't have the starter spell — give them heal + mana items guaranteed
        library_loot.append(get_spell_book(heal))
        library_loot.append({
            "name": "Arcane Mana Crystal",
            "type": "consumable_mana_capacity",
            "effect": {"mana_capacity": 20},
            "rarity": "uncommon"
        })
        library_loot.append({
            "name": "Mana Potion",
            "type": "consumable_mana",
            "effect": {"mana": 25},
            "rarity": "common"
        })

        # Small 25% chance at a second random spell (anything except heal)
        other_spells = [s for s in [fireball, lightning, ice_blast, shield]
                        if s.name.lower() not in known_spell_names]
        if other_spells and random.random() < 0.25:
            library_loot.append(get_spell_book(random.choice(other_spells)))

    else:
        # Player already has heal — chance at any other spell they don't know yet
        unknown_spells = [s for s in [fireball, lightning, ice_blast, shield]
                          if s.name.lower() not in known_spell_names]

        if unknown_spells:
            # 60% chance to get a new spell
            if random.random() < 0.60:
                library_loot.append(get_spell_book(random.choice(unknown_spells)))

                # Extra 20% chance at a second new spell
                remaining = [s for s in unknown_spells
                             if s.name.lower() != library_loot[0]["effect"]["spell"].name.lower()]
                if remaining and random.random() < 0.20:
                    library_loot.append(get_spell_book(random.choice(remaining)))

    # Always add 1-2 random additional loot items
    additional_loot = get_additional_loot()
    loot_count = random.randint(1, 2)
    library_loot.extend(random.sample(additional_loot, min(loot_count, len(additional_loot))))

    return library_loot

def get_new_spells(known_spells):
    """Returns a list of new spells that the player does not know."""
    all_spells = [fireball, heal, lightning, ice_blast, shield]
    return [spell for spell in all_spells if spell.name not in known_spells]

def get_spell_book(spell):
    """Returns a spell book item for the given spell."""
    return {
        "name": f"Spell Book: {spell.name.capitalize()}",
        "type": "spell_book",
        "effect": {"spell": spell},
        "rarity": "uncommon"
    }

def get_additional_loot():
    """Returns a pool of additional loot that can be found in the library."""
    return [
        {"name": "Dusty Health Potion", "type": "consumable_health", "effect": {"health": 20}, "rarity": "common"},
        {"name": "Mana Potion", "type": "consumable_mana", "effect": {"mana": 20}, "rarity": "common"},
        {"name": "Arcane Scroll", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 10}, "rarity": "uncommon"},
        {"name": "Ancient Tome of Vitality", "type": "consumable_health_capacity", "effect": {"health_capacity": 10}, "rarity": "uncommon"},
        {"name": "Scholar's Robe", "type": "armor", "slot": "chestplate", "effect": {"defense": 1}, "rarity": "common"},
    ]

def get_treasure_chest_loot():
    """Generates random treasure chest loot."""
    treasure_chest_loot = [
        {"name": "Rusty Sword", "type": "weapon", "effect": {"attack": 5}, "rarity": "common"},
        {"name": "Lesser Health Potion", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"},
        {"name": "Lesser Mana Potion", "type": "consumable_mana", "effect": {"mana": 15}, "rarity": "common"}
    ]
    loot_count = random.randint(2, 3)
    return random.sample(treasure_chest_loot, loot_count)

def get_kitchen_loot():
    """Generates random kitchen loot."""
    kitchen_loot = [
        {"name": "Stale Bread", "type": "consumable_health", "effect": {"health": 5}, "rarity": "common"},
        {"name": "Hearty Stew", "type": "consumable_health", "effect": {"health": 25}, "rarity": "uncommon"},
        {"name": "Old Wine", "type": "consumable_mana", "effect": {"mana": 15}, "rarity": "common"},
        {"name": "Dried Meat", "type": "consumable_health", "effect": {"health": 10}, "rarity": "common"},
        {"name": "Mysterious Herb", "type": "consumable_health_capacity", "effect": {"health_capacity": 5}, "rarity": "uncommon"},
        {"name": "Kitchen Knife", "type": "weapon", "effect": {"attack": 2}, "rarity": "common"},
    ]
    loot_count = random.randint(2, 3)
    return random.sample(kitchen_loot, min(loot_count, len(kitchen_loot)))

def get_dining_hall_loot():
    """Generates random dining hall loot."""
    dining_hall_loot = [
        {"name": "Silver Goblet of Healing", "type": "consumable_health", "effect": {"health": 20}, "rarity": "uncommon"},
        {"name": "Enchanted Wine", "type": "consumable_mana", "effect": {"mana": 25}, "rarity": "uncommon"},
        {"name": "Leftover Feast", "type": "consumable_health", "effect": {"health": 30}, "rarity": "uncommon"},
        {"name": "Ornate Dagger", "type": "weapon", "effect": {"attack": 3}, "rarity": "common"},
        {"name": "Servant's Shield", "type": "armor", "slot": "shield", "effect": {"defense": 1}, "rarity": "common"},
    ]
    loot_count = random.randint(2, 3)
    return random.sample(dining_hall_loot, min(loot_count, len(dining_hall_loot)))

def get_garden_loot():
    """Generates random garden loot."""
    garden_loot = [
        {"name": "Healing Herb", "type": "consumable_health", "effect": {"health": 15}, "rarity": "common"},
        {"name": "Moonpetal Flower", "type": "consumable_mana", "effect": {"mana": 20}, "rarity": "uncommon"},
        {"name": "Enchanted Seed", "type": "consumable_health_capacity", "effect": {"health_capacity": 10}, "rarity": "uncommon"},
        {"name": "Mystic Mushroom", "type": "consumable_mana_capacity", "effect": {"mana_capacity": 10}, "rarity": "uncommon"},
        {"name": "Thorny Branch", "type": "weapon", "effect": {"attack": 2}, "rarity": "common"},
        {"name": "Bark Shield", "type": "armor", "slot": "shield", "effect": {"defense": 1}, "rarity": "common"},
    ]
    loot_count = random.randint(2, 3)
    return random.sample(garden_loot, min(loot_count, len(garden_loot)))

def get_armory_loot():
    """Generates loot found in the armory."""
    possible_loot = [
        {"name": "Iron Sword", "type": "weapon", "effect": {"attack": 3}, "rarity": "common"},
        {"name": "Steel Shield", "type": "armor", "slot": "shield", "effect": {"defense": 2}, "rarity": "common"},
        {"name": "Battle Axe", "type": "weapon", "effect": {"attack": 5}, "rarity": "uncommon"},
        {"name": "Chainmail Vest", "type": "armor", "slot": "chestplate", "effect": {"defense": 2}, "rarity": "uncommon"},
        {"name": "War Hammer", "type": "weapon", "effect": {"attack": 4}, "rarity": "uncommon"},
        {"name": "Leather Gauntlets", "type": "armor", "slot": "boots", "effect": {"defense": 1}, "rarity": "common"},
        {"name": "Rusty Dagger", "type": "weapon", "effect": {"attack": 2}, "rarity": "common"},
        {"name": "Knight's Helm", "type": "armor", "slot": "helmet", "effect": {"defense": 2}, "rarity": "common"},
        {"name": "Health Potion", "type": "consumable_health", "effect": {"health": 20}, "rarity": "common"},
    ]
    num_items = random.randint(2, 4)
    return random.sample(possible_loot, min(num_items, len(possible_loot)))