import random
from loot import generate_treasure_chest_loot
from utils.helpers import format_output, validate_input, prompt_continue

def handle_treasure_room(game):
    """Handles the treasure room mechanics."""
    if not game.treasure_room_looted:
        move_to_chest = validate_input(f"Do you want to open the chest? (yes/no) > ", ["yes", "no"])
        if move_to_chest == "yes":
            loot_items = generate_treasure_chest_loot()
            for loot in loot_items:
                if loot["type"].startswith("consumable"):
                    effect_type = list(loot["effect"].keys())[0]
                    loot_description = f"{loot['name']} (+{loot['effect'][effect_type]} {effect_type.capitalize()})"
                else:
                    loot_description = f"{loot['name']} ({', '.join([f'{k}: {v}' for k, v in loot['effect'].items()])})"
                game.game_text.append(format_output(f"You found {loot_description}"))
                take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
                if take_loot == "yes":
                    game.player.inventory.append(loot)
                    game.game_text.append(format_output(f"You took the {loot['name']}!"))
                else:
                    game.game_text.append(format_output(f"You left the {loot['name']} behind."))
            game.treasure_room_looted = True
        else:
            game.game_text.append(format_output(f"You left the chest unopened."))
    else:
        game.game_text.append(format_output(f"The chest is empty."))
    game.render_screen()
    prompt_continue()