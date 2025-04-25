from items.loot import get_dining_hall_loot
from utils.helpers import format_output, validate_input, prompt_continue

def handle_dining_hall_loot(game):
    """Handles the loot generation and interaction in the dining hall."""
    if not game.dining_hall_looted:
        loot_items = get_dining_hall_loot()
        for loot in loot_items:
            if loot["type"].startswith("consumable"):
                effect_type = list(loot["effect"].keys())[0]
                loot_description = f"{loot['name']} (+{loot['effect'][effect_type]} {effect_type.replace('_', ' ').capitalize()})"
            else:
                loot_description = f"{loot['name']} ({', '.join([f'{k}: {v}' for k, v in loot['effect'].items()])})"
            game.game_text.append(format_output(f"You found {loot_description}"))
            take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                game.player.inventory.append(loot)
                game.game_text.append(format_output(f"You took the {loot['name']}!"))
            else:
                game.game_text.append(format_output(f"You left the {loot['name']} behind."))
        game.dining_hall_looted = True
    else:
        game.game_text.append(format_output("The dining hall has already been looted."))
    game.render_screen()
    prompt_continue()