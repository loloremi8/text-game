from items.loot import get_armory_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_armory_loot(game):
    """Handles searching the armory."""
    room = game.rooms["armory"]
    if room.looted:
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
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
