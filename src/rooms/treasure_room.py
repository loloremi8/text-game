from items.loot import get_treasure_chest_loot
from utils.helpers import format_output, validate_input, prompt_continue, format_loot_description

def handle_treasure_room(game):
    """Handles the treasure room interaction."""
    if game.treasure_room_looted:
        game.game_text = format_output("The chest is empty. You've already looted it.")
        game.render_screen()
        prompt_continue()
        return

    game.game_text = format_output("You approach the chest and open it...")
    game.render_screen()
    prompt_continue()

    loot_items = get_treasure_chest_loot()
    if not loot_items:
        game.game_text = format_output("The chest is empty!")
        game.render_screen()
        prompt_continue()
        game.treasure_room_looted = True
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

    game.treasure_room_looted = True
    game.game_text = format_output("The chest is now empty.")
    game.render_screen()
    prompt_continue()