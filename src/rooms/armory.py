from items.loot import get_armory_loot
from utils.helpers import validate_input, prompt_continue, format_loot_description

def handle_armory_loot(game):
    """Handles searching the armory."""
    if game.armory_looted:
        game.game_text = "You've already searched the armory."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You search through the weapon racks and armor stands..."
    game.render_screen()
    prompt_continue()

    loot_items = get_armory_loot()
    if not loot_items:
        game.game_text = "You find nothing useful."
        game.render_screen()
        prompt_continue()
        game.armory_looted = True
        return

    for loot in loot_items:
        loot_description = format_loot_description(loot)
        game.game_text = f"You found: {loot_description}"
        game.render_screen()

        take = validate_input(
            f"Take the {loot['name']}? (yes/no) > ",
            ["yes", "no"],
            {"y": "yes", "n": "no"}
        )
        if take == "yes":
            game.player.inventory.append(loot)
            game.game_text = f"You took the {loot['name']}!"
        else:
            game.game_text = f"You left the {loot['name']} behind."

        game.render_screen()
        prompt_continue()

    game.armory_looted = True