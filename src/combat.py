import random
from loot import generate_loot
from utils.helpers import format_output, prompt_continue, validate_input

def combat(game, player, monsters):
    """Handles combat between the player and a list of monsters."""
    for monster in monsters:
        game.game_text.append(format_output(f"A wild {monster.name} appears!"))
        game.render_screen(monster)
        prompt_continue()

        while player.health > 0 and monster.health > 0:
            # Display player and monster stats
            game.render_screen(monster)

            # Ask the player what they want to do next
            action = validate_input("What do you want to do? (fight/run/inventory) > ", ["fight", "run", "inventory"])
            if action == "run":
                game.game_text.append(format_output("You chose to run away!"))
                game.render_screen(monster)
                return False  # Player ran away
            elif action == "inventory":
                game.manage_inventory()
                game.render_screen(monster)
                continue
            elif action == "fight":
                attack_type = validate_input("How do you want to attack? (melee/spell) > ", ["melee", "spell"])
                if attack_type == "spell":
                    if player.spells:
                        print("You can cast the following spells:")
                        for spell in player.spells:
                            print(f">{spell.name} (Mana cost: {spell.mana_cost}, Effect: {spell.spell_type} {spell.effect})")
                        spell_name = input("Enter the name of the spell you want to cast: ").strip().lower()
                        spell_result = player.cast_spell(spell_name)
                        if spell_result:
                            if spell_result["type"] == "damage":
                                monster.health -= spell_result["amount"]
                                game.game_text.append(format_output(f"You cast {spell_name} and deal {spell_result['amount']} damage to the {monster.name}."))
                            elif spell_result["type"] == "heal":
                                game.game_text.append(format_output(f"You cast {spell_name} and heal {spell_result['amount']} health."))
                    else:
                        game.game_text.append(format_output("You don't know any spells."))
                    game.render_screen(monster)
                    continue

            # Player's and monster's damage
            player.damage = random.randint(1, player.attack)
            monster.health -= player.damage
            monster.damage = max(0, random.randint(1, monster.attack) - player.defense)
            player.health -= monster.damage

            # Display combat results
            game.game_text.append(format_output(f"You attack the {monster.name}!\nYou deal {player.damage} damage to the {monster.name}.\n\nThe {monster.name} attacks you!\nThe {monster.name} deals {monster.damage} damage to you."))

            # Check if the player or monster has been defeated
            game.render_screen(monster)
            if monster.health <= 0:
                game.game_text.append(format_output(f"You have defeated the {monster.name}!"))
                # Generate loot based on the defeated monster
                loot_items = generate_loot(monster)
                if loot_items:
                    for loot in loot_items:
                        if loot["type"].startswith("consumable"):
                            effect_type = list(loot["effect"].keys())[0]
                            loot_description = f"{loot['name']} (+{loot['effect'][effect_type]} {effect_type.capitalize()})"
                        else:
                            loot_description = f"{loot['name']} ({', '.join([f'{k}: {v}' for k, v in loot['effect'].items()])})"
                        game.game_text.append(format_output(f"You found {loot_description}"))
                        take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
                        if take_loot == "yes":
                            player.inventory.append(loot)
                            game.game_text.append(format_output(f"You took the {loot['name']}!"))
                        else:
                            game.game_text.append(format_output(f"You left the {loot['name']} behind."))
                game.render_screen(monster)
                break
            if player.health <= 0:
                game.game_text.append(format_output("You have been defeated!"))
                game.render_screen(monster)
                return False  # Player defeated

            prompt_continue()

    return True  # All monsters defeated