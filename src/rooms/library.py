from loot import generate_library_loot
from magic import fireball, heal, lightning, ice_blast, shield
from utils.helpers import format_output, validate_input, prompt_continue

def handle_library_loot(game):
    """Handles the loot generation and interaction in the library room."""
    loot_items = generate_library_loot(game.player)
    for loot in loot_items:
        if loot["type"] == "consumable_spell":
            spell_name = loot["effect"]["spell"]
            spell = next(spell for spell in [fireball, heal, lightning, ice_blast, shield] if spell.name == spell_name)
            game.player.spells.append(spell)
            print(f"You read through the old books and grimmoires and you learned a new spell: {spell_name}!")
        elif loot["type"].startswith("consumable"):
            effect_type = list(loot["effect"].keys())[0]
            loot_description = f"{loot['name']} (+{loot['effect'][effect_type]} {effect_type.replace('_', ' ').capitalize()})"
            game.game_text.append(format_output(f"You found {loot_description}"))
            take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                game.player.inventory.append(loot)
                game.game_text.append(format_output(f"You took the {loot['name']}!"))
            else:
                game.game_text.append(format_output(f"You left the {loot['name']} behind."))
        else:
            loot_description = f"{loot['name']} ({', '.join([f'{k}: {v}' for k, v in loot['effect'].items()])})"
            game.game_text.append(format_output(f"You found {loot_description}"))
            take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                game.player.inventory.append(loot)
                game.game_text.append(format_output(f"You took the {loot['name']}!"))
            else:
                game.game_text.append(format_output(f"You left the {loot['name']} behind."))
    game.library_looted = True
    game.render_screen()
    prompt_continue()