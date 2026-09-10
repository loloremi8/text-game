from items.loot import get_library_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_library_loot(game):
    """Handles searching the library."""
    room = game.rooms["library"]
    if room.looted:
        game.game_text = "You've already searched the library."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You search through the dusty shelves..."
    game.render_screen()
    prompt_continue()

    loot_items = get_library_loot(game.player)
    if not loot_items:
        game.game_text = "You find nothing of interest."
        game.render_screen()
        prompt_continue()
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
