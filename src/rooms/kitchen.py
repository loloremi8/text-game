from items.loot import get_kitchen_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_kitchen_loot(game):
    """Handles searching the kitchen."""
    room = game.rooms["kitchen"]
    if room.looted:
        game.game_text = "You've already searched the kitchen."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You rummage through the old kitchen..."
    game.render_screen()
    prompt_continue()

    loot_items = get_kitchen_loot()
    if not loot_items:
        game.game_text = "You find nothing edible or useful."
        game.render_screen()
        prompt_continue()
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
