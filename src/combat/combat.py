from combat import rules
from combat.monsters import generate_loot
from items.loot_flow import offer_loot
from utils.helpers import prompt_continue, validate_input

def combat(game, player, monsters):
    """Handles combat between the player and a list of monsters."""
    player.shield_pool = 0  # a barrier does not survive between encounters

    for monster in monsters:
        game.game_text = f"A {monster.name} appears!"
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
                game.game_text = "You chose to run away!"
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
                            game.game_text = "You didn't enter a spell name!"
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
                                    dealt = rules.spell_damage(spell_result["amount"], monster.defense)
                                    monster.health -= dealt
                                    game.game_text = f"You cast {spell_to_cast.name.capitalize()} and deal {dealt} damage to the {monster.name}."
                                elif spell_result["type"] == "heal":
                                    game.game_text = f"You cast {spell_to_cast.name.capitalize()} and heal {spell_result['amount']} health."
                                elif spell_result["type"] == "shield":
                                    player.shield_pool = max(player.shield_pool, spell_result["amount"])
                                    game.game_text = f"You cast {spell_to_cast.name.capitalize()} and raise a barrier worth {player.shield_pool} damage."

                                game.render_screen(monster)
                                prompt_continue()
                            else:
                                game.game_text = "The spell failed! (Not enough mana?)"
                                game.render_screen(monster)
                                prompt_continue()
                                continue
                        else:
                            game.game_text = f"'{spell_input}' is not a valid spell!"
                            game.render_screen(monster)
                            prompt_continue()
                            continue
                    else:
                        game.game_text = "You don't know any spells."
                        game.render_screen(monster)
                        prompt_continue()
                        continue
                else:
                    # Crit chance is applied inside the rules helper
                    damage_dealt, is_crit = rules.melee_damage(
                        player.attack, monster.defense, player.crit_chance
                    )
                    monster.health -= damage_dealt

                    if is_crit:
                        game.game_text = f"CRITICAL HIT! You attack the {monster.name} and deal {damage_dealt} damage."
                    else:
                        game.game_text = f"You attack the {monster.name} and deal {damage_dealt} damage."

                    game.render_screen(monster)
                    prompt_continue()

                # Monster's turn (only if monster is still alive)
                if monster.health > 0:
                    raw_damage = rules.melee_damage(monster.attack, player.defense)[0]
                    player.shield_pool, monster_damage = rules.absorb(player.shield_pool, raw_damage)
                    player.health -= monster_damage
                    if monster_damage < raw_damage:
                        game.game_text = (f"The {monster.name} attacks you and deals {monster_damage} damage. "
                                          f"Your magic shield absorbs {raw_damage - monster_damage}.")
                    else:
                        game.game_text = f"The {monster.name} attacks you and deals {monster_damage} damage."

                    game.render_screen(monster)
                    prompt_continue()

                # Check if monster defeated
                if monster.health <= 0:
                    game.game_text = f"You have defeated the {monster.name}!"
                    game.render_screen(monster)
                    offer_loot(game, generate_loot(monster), monster)
                    break

                # Check if player defeated
                if player.health <= 0:
                    game.game_text = "You have been defeated! Game Over."
                    game.render_screen(monster)
                    prompt_continue()
                    return False

    return True