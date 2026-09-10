from items.loot import get_treasure_chest_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue

def handle_treasure_room(game):
    """Handles the treasure room interaction."""
    room = game.rooms["treasure_room"]
    if room.looted:
        game.game_text = "The chest is empty. You've already looted it."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You approach the chest and open it..."
    game.render_screen()
    prompt_continue()

    loot_items = get_treasure_chest_loot()
    if not loot_items:
        game.game_text = "The chest is empty!"
        game.render_screen()
        prompt_continue()
        room.looted = True
        return

    offer_loot(game, loot_items)
    room.looted = True
    game.game_text = "The chest is now empty."
    game.render_screen()
    prompt_continue()
