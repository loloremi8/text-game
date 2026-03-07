from items.loot import get_garden_loot
from utils.helpers import format_output, validate_input, prompt_continue, format_loot_description

def handle_garden_loot(game):
    """Handles searching the garden."""
    if game.garden_looted:
        game.game_text = format_output("You've already searched the garden.")
        game.render_screen()
        prompt_continue()
        return

    game.game_text = format_output("You search among the overgrown plants and crumbling statues...")
    game.render_screen()
    prompt_continue()

    loot_items = get_garden_loot()
    if not loot_items:
        game.game_text = format_output("You find nothing hidden in the garden.")
        game.render_screen()
        prompt_continue()
        game.garden_looted = True
        return

    for loot in loot_items:
        loot_description = format_loot_description(loot)
        game.game_text = format_output(f"You found: {loot_description}")
        game.render_screen()

        take = validate_input(
            f"Take the {loot['name']}? (yes/no) > ",
            ["yes", "no"],
            {"y": "yes", "n": "no"}
        )
        if take == "yes":
            game.player.inventory.append(loot)
            game.game_text = format_output(f"You took the {loot['name']}!")
        else:
            game.game_text = format_output(f"You left the {loot['name']} behind.")

        game.render_screen()
        prompt_continue()

    game.garden_looted = True