import shutil
from utils.helpers import clear_screen, prompt_continue, format_loot_description


def get_terminal_width():
    return shutil.get_terminal_size((80, 24)).columns


EQUIPMENT_SLOTS = ["weapon", "helmet", "chestplate", "shield", "boots"]


def manage_inventory(game):
    """Manages the player's inventory, equipment, and spells."""
    while True:
        clear_screen()
        term_width = get_terminal_width()
        print("─" * term_width)
        print("  INVENTORY & EQUIPMENT")
        print("─" * term_width)

        # Show player stats
        print()
        stats = game.player.display_status()
        for line in stats.split("\n"):
            print(f"  {line}")
        print()

        # Show equipped items
        print("─" * term_width)
        print("  EQUIPPED:")
        for slot in EQUIPMENT_SLOTS:
            item = game.player.equipped.get(slot)
            label = slot.capitalize()
            if item:
                if slot == "weapon":
                    print(f"    {label}: {item['name']} (Attack: +{item['effect']['attack']})")
                else:
                    print(f"    {label}: {item['name']} (Defense: +{item['effect']['defense']})")
            else:
                print(f"    {label}: None")
        print()

        # Show known spells
        if game.player.spells:
            print("  SPELLS:")
            for spell in game.player.spells:
                print(f"    > {spell.name.capitalize()} (Mana: {spell.mana_cost}, {spell.spell_type.capitalize()}: {spell.effect})")
            print()

        print("─" * term_width)
        print("  ITEMS:")

        if not game.player.inventory:
            print("\n    Your inventory is empty.\n")
            prompt_continue()
            break

        for i, item in enumerate(game.player.inventory, 1):
            print(f"    [{i}] {format_loot_description(item)}")

        print()
        print("  [u] Unequip an item")
        print("  [t] Trash an item")
        print("  [0] Close inventory")
        print()

        choice = input("  Choose an item to use/equip > ").strip().lower()
        if choice == "0":
            break
        elif choice == "t":
            trash_item(game)
            continue
        elif choice == "u":
            unequip_item(game)
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(game.player.inventory):
            item = game.player.inventory[int(choice) - 1]
            game.player.use_item(item["name"])
            prompt_continue()
        else:
            print("  Invalid choice. Please try again.")
            prompt_continue()


def unequip_item(game):
    """Allows the player to unequip an item from any slot."""
    clear_screen()
    term_width = get_terminal_width()
    print("─" * term_width)
    print("  UNEQUIP ITEM")
    print("─" * term_width)

    options = []
    for slot in EQUIPMENT_SLOTS:
        item = game.player.equipped.get(slot)
        if item:
            options.append((slot, item))
            idx = len(options)
            label = slot.capitalize()
            if slot == "weapon":
                print(f"  [{idx}] {label}: {item['name']} (Attack: +{item['effect']['attack']})")
            else:
                print(f"  [{idx}] {label}: {item['name']} (Defense: +{item['effect']['defense']})")

    if not options:
        print("\n  Nothing equipped to remove.\n")
        prompt_continue()
        return

    print()
    print("  [0] Back")
    print()

    choice = input("  Which item to unequip? > ").strip()
    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            slot, item = options[idx]
            if slot == "weapon":
                game.player.attack -= item["effect"]["attack"]
            else:
                game.player.defense -= item["effect"]["defense"]
            game.player.equipped[slot] = None
            game.player.inventory.append(item)
            print(f"  You unequipped {item['name']}.")
            prompt_continue()
        else:
            print("  Invalid choice.")
            prompt_continue()
    except ValueError:
        print("  Invalid choice.")
        prompt_continue()


def trash_item(game):
    """Allows the player to trash an item from the inventory."""
    while True:
        clear_screen()
        term_width = get_terminal_width()
        print("─" * term_width)
        print("  TRASH AN ITEM")
        print("─" * term_width)

        if not game.player.inventory:
            print("\n  Nothing to trash.\n")
            prompt_continue()
            break

        for i, item in enumerate(game.player.inventory, 1):
            print(f"  [{i}] {format_loot_description(item)}")

        print()
        print("  [0] Back")
        print()

        choice = input("  Which item do you want to trash? > ").strip().lower()
        if choice == "0":
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(game.player.inventory):
                item = game.player.inventory.pop(idx)
                print(f"  You trashed {item['name']}.")
                prompt_continue()
                break
            else:
                print("  Invalid choice, please try again.")
                prompt_continue()
        except ValueError:
            print("  Invalid choice, please try again.")
            prompt_continue()