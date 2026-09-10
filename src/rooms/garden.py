from items.loot import get_garden_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_garden_loot(game):
    """Handles searching the garden."""
    room = game.rooms["garden"]
    if room.looted:
        game.game_text = "You've already searched the garden."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You search among the overgrown plants and crumbling statues..."
    game.render_screen()
    prompt_continue()

    loot_items = get_garden_loot()
    if not loot_items:
        game.game_text = "You find nothing hidden in the garden."
        game.render_screen()
        prompt_continue()
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
