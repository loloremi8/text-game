import os

def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def format_output(text):
    """Formats the output text."""
    return text

def prompt_continue():
    """Prompts the user to press Enter to continue."""
    input("\nPress Enter to continue...")

def validate_input(prompt, valid_options, aliases=None):
    """Validates user input against a list of valid options, with optional short aliases."""
    if aliases is None:
        aliases = {}
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        elif choice in aliases:
            return aliases[choice]
        else:
            options_display = []
            for opt in valid_options:
                short = [k for k, v in aliases.items() if v == opt]
                if short:
                    options_display.append(f"{opt}({short[0]})")
                else:
                    options_display.append(opt)
            print(f"Invalid input. Please choose: {', '.join(options_display)}")

def format_loot_description(loot):
    """Formats a loot item into a readable description string."""
    rarity = loot.get("rarity", "common").capitalize()
    if loot["type"] == "spell_book":
        spell = loot["effect"]["spell"]
        return f"[{rarity}] {loot['name']} (Teaches: {spell.name.capitalize()} - {spell.spell_type.capitalize()} {spell.effect})"
    elif loot["type"] == "consumable_health":
        return f"[{rarity}] {loot['name']} (Restores {loot['effect']['health']} health)"
    elif loot["type"] == "consumable_mana":
        return f"[{rarity}] {loot['name']} (Restores {loot['effect']['mana']} mana)"
    elif loot["type"] == "consumable_health_capacity":
        return f"[{rarity}] {loot['name']} (Max health +{loot['effect']['health_capacity']})"
    elif loot["type"] == "consumable_mana_capacity":
        return f"[{rarity}] {loot['name']} (Max mana +{loot['effect']['mana_capacity']})"
    elif loot["type"] == "weapon":
        return f"[{rarity}] {loot['name']} (Attack: +{loot['effect']['attack']})"
    elif loot["type"] == "armor":
        slot = loot.get("slot", "armor").capitalize()
        return f"[{rarity}] {loot['name']} ({slot}, Defense: +{loot['effect']['defense']})"
    else:
        return f"[{rarity}] {loot['name']}"