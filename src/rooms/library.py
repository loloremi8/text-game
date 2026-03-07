from items.loot import get_library_loot
from utils.helpers import format_output, validate_input, prompt_continue, format_loot_description

def handle_library_loot(game):
    """Handles searching the library."""
    game.game_text = format_output("You search through the dusty shelves...")
    game.render_screen()
    prompt_continue()

    loot_items = get_library_loot(game.player)
    if not loot_items:
        game.game_text = format_output("You find nothing of interest.")
        game.render_screen()
        prompt_continue()
        game.library_looted = True
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

    game.library_looted = True