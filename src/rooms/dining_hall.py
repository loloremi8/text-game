from items.loot import get_dining_hall_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_dining_hall_loot(game):
    """Handles searching the dining hall."""
    room = game.rooms["dining_hall"]
    if room.looted:
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
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
