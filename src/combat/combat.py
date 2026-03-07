import random
from combat.monsters import generate_loot
from utils.helpers import format_output, prompt_continue, validate_input, format_loot_description

def combat(game, player, monsters):
    """Handles combat between the player and a list of monsters."""
    for monster in monsters:
        game.game_text = format_output(f"A {monster.name} appears!")
        game.render_screen(monster)
        prompt_continue()

        while player.health > 0 and monster.health > 0:
            game.render_screen(monster)

            action = validate_input(
                "What do you want to do? (fight/run/inventory) > ",
                ["fight", "run", "inventory"],
                {"f": "fight", "r": "run", "i": "inventory"}
            )
            if action == "run":
                game.game_text = format_output("You chose to run away!")
                game.render_screen(monster)
                return False
            elif action == "inventory":
                game.manage_inventory()
                game.render_screen(monster)
                continue
            elif action == "fight":
                attack_type = validate_input(
                    "How do you want to attack? (melee/spell) > ",
                    ["melee", "spell"],
                    {"m": "melee", "s": "spell"}
                )

                if attack_type == "spell":
                    if player.spells:
                        print("\nYou can cast the following spells:")
                        for spell in player.spells:
                            print(f"  > {spell.name} (Mana cost: {spell.mana_cost}, Effect: {spell.spell_type} {spell.effect})")

                        spell_input = input("\nEnter the spell name or first letter: ").strip().lower()

                        if not spell_input:
                            game.game_text = format_output("You didn't enter a spell name!")
                            game.render_screen(monster)
                            prompt_continue()
                            continue

                        spell_to_cast = None
                        for spell in player.spells:
                            if spell.name.lower() == spell_input or spell.name.lower().startswith(spell_input):
                                spell_to_cast = spell
                                break

                        if spell_to_cast:
                            spell_result = player.cast_spell(spell_to_cast.name.lower())
                            if spell_result:
                                if spell_result["type"] == "damage":
                                    monster.health -= spell_result["amount"]
                                    game.game_text = format_output(f"You cast {spell_to_cast.name.capitalize()} and deal {spell_result['amount']} damage to the {monster.name}.")
                                elif spell_result["type"] == "heal":
                                    game.game_text = format_output(f"You cast {spell_to_cast.name.capitalize()} and heal {spell_result['amount']} health.")

                                game.render_screen(monster)
                                prompt_continue()
                            else:
                                game.game_text = format_output("The spell failed! (Not enough mana?)")
                                game.render_screen(monster)
                                prompt_continue()
                                continue
                        else:
                            game.game_text = format_output(f"'{spell_input}' is not a valid spell!")
                            game.render_screen(monster)
                            prompt_continue()
                            continue
                    else:
                        game.game_text = format_output("You don't know any spells.")
                        game.render_screen(monster)
                        prompt_continue()
                        continue
                else:
                    damage_dealt = max(0, random.randint(1, player.attack) - monster.defense)

                    # Rogue crit chance
                    is_crit = player.crit_chance > 0 and random.random() < player.crit_chance
                    if is_crit:
                        damage_dealt *= 2

                    monster.health -= damage_dealt

                    if is_crit:
                        game.game_text = format_output(f"CRITICAL HIT! You attack the {monster.name} and deal {damage_dealt} damage.")
                    else:
                        game.game_text = format_output(f"You attack the {monster.name} and deal {damage_dealt} damage.")

                    game.render_screen(monster)
                    prompt_continue()

                # Monster's turn (only if monster is still alive)
                if monster.health > 0:
                    monster_damage = max(0, random.randint(1, monster.attack) - player.defense)
                    player.health -= monster_damage
                    game.game_text = format_output(f"The {monster.name} attacks you and deals {monster_damage} damage.")

                    game.render_screen(monster)
                    prompt_continue()

                # Check if monster defeated
                if monster.health <= 0:
                    game.game_text = format_output(f"You have defeated the {monster.name}!")
                    game.render_screen(monster)
                    loot_items = generate_loot(monster)
                    if loot_items:
                        for loot in loot_items:
                            loot_description = format_loot_description(loot)
                            game.game_text = format_output(f"You found: {loot_description}")
                            game.render_screen(monster)
                            take_loot = validate_input(
                                f"Do you want to take the {loot['name']}? (yes/no) > ",
                                ["yes", "no"],
                                {"y": "yes", "n": "no"}
                            )
                            if take_loot == "yes":
                                player.inventory.append(loot)
                                game.game_text = format_output(f"You took the {loot['name']}!")
                            else:
                                game.game_text = format_output(f"You left the {loot['name']} behind.")
                            game.render_screen(monster)
                    prompt_continue()
                    break

                # Check if player defeated
                if player.health <= 0:
                    game.game_text = format_output("You have been defeated! Game Over.")
                    game.render_screen(monster)
                    prompt_continue()
                    return False

    return True