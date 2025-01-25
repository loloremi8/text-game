import random
from monsters import generate_loot
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
            action = validate_input("What do you want to do? (fight/run) > ", ["fight", "run"])
            if action == "run":
                game.game_text.append(format_output("You chose to run away!"))
                game.render_screen(monster)
                return False  # Player ran away

            # Player's and monster's damage
            player.damage = random.randint(1, player.attack)
            monster.health -= player.damage
            monster.damage = random.randint(1, monster.attack)
            player.health -= monster.damage

            # Display combat results
            game.game_text.append(format_output(f"You attack the {monster.name}!\nYou deal {player.damage} damage to the {monster.name}.\n\nThe {monster.name} attacks you!\nThe {monster.name} deals {monster.damage} damage to you."))

            # Check if the player or monster has been defeated
            game.render_screen(monster)
            if monster.health <= 0:
                game.game_text.append(format_output(f"You have defeated the {monster.name}!"))
                # Generate loot based on the defeated monster
                loot = generate_loot(monster)
                if loot:
                    game.game_text.append(format_output(f"You found {loot['name']}!"))
                    game.render_screen(monster)
                    take_loot = validate_input("Do you want to take the loot? (yes/no) > ", ["yes", "no"])
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
                return True  # Player defeated

            prompt_continue()

    return True  # All monsters defeated