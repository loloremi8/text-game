import shutil
from utils.helpers import clear_screen, prompt_continue, format_loot_description


def get_terminal_width():
    return shutil.get_terminal_size((80, 24)).columns


EQUIPMENT_SLOTS = ["weapon", "helmet", "chestplate", "shield", "boots"]


STACKABLE_TYPES = {
    "consumable_health", "consumable_mana",
    "consumable_health_capacity", "consumable_mana_capacity",
}


def canonical_effect(effect):
    """Sorted tuple of (key, value) pairs for an item effect."""
    if not effect:
        return ()
    return tuple(sorted(effect.items()))


def stack_signature(item):
    """Identity of a stack: (type, name, slot, canonical(effect))."""
    return (item["type"], item["name"], item.get("slot"), canonical_effect(item.get("effect")))


def format_stack_description(stack):
    """Formats a stack into a readable description, showing the count when > 1."""
    description = format_loot_description(stack["item"])
    if stack["count"] > 1:
        return f"{description} x{stack['count']}"
    return description


class Inventory:
    """A stack-based inventory. Each stack is {"item": <item dict>, "count": int}."""

    def __init__(self):
        self.stacks = []

    def add(self, item, count=1):
        """Adds an item, merging into an existing stack when the type stacks and the signature matches."""
        if item["type"] in STACKABLE_TYPES:
            signature = stack_signature(item)
            for stack in self.stacks:
                if stack_signature(stack["item"]) == signature:
                    stack["count"] += count
                    return
        self.stacks.append({"item": item, "count": count})

    def remove(self, index, count=1):
        """Removes up to count items from the stack at index. Returns True if anything was removed."""
        if index < 0 or index >= len(self.stacks):
            return False
        stack = self.stacks[index]
        if count >= stack["count"]:
            self.stacks.pop(index)
        else:
            stack["count"] -= count
        return True

    def total_items(self):
        """Sum of the counts across every stack."""
        total = 0
        for stack in self.stacks:
            total += stack["count"]
        return total

    def __len__(self):
        """Number of stacks, not items."""
        return len(self.stacks)

    def __iter__(self):
        for stack in self.stacks:
            yield stack

    def __bool__(self):
        return len(self.stacks) > 0


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

        for i, stack in enumerate(game.player.inventory, 1):
            print(f"    [{i}] {format_stack_description(stack)}")

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
            game.player.use_item(int(choice) - 1)
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
            game.player.equipped[slot] = None
            game.player.inventory.add(item)
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

        for i, stack in enumerate(game.player.inventory, 1):
            print(f"  [{i}] {format_stack_description(stack)}")

        print()
        print("  [0] Back")
        print()

        choice = input("  Which item do you want to trash? > ").strip().lower()
        if choice == "0":
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(game.player.inventory):
                item = game.player.inventory.stacks[idx]["item"]
                game.player.inventory.remove(idx, 1)
                print(f"  You trashed {item['name']}.")
                prompt_continue()
            else:
                print("  Invalid choice, please try again.")
                prompt_continue()
        except ValueError:
            print("  Invalid choice, please try again.")
            prompt_continue()
