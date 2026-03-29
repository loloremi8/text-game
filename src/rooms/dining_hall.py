from items.loot import get_dining_hall_loot
from utils.helpers import validate_input, prompt_continue, format_loot_description

def handle_dining_hall_loot(game):
    """Handles searching the dining hall."""
    if game.dining_hall_looted:
        game.game_text = "You've already searched the dining hall."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You search the long dining tables and cabinets..."
    game.render_screen()
    prompt_continue()

    loot_items = get_dining_hall_loot()
    if not loot_items:
        game.game_text = "You find nothing of value."
        game.render_screen()
        prompt_continue()
        game.dining_hall_looted = True
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

    game.dining_hall_looted = True