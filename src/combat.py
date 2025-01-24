import random
from utils.helpers import format_output, prompt_continue, validate_input

def combat(game, player, monster):
    """Handles combat between the player and a monster."""
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
            break

        # Player's damage and monster's damage
        player.damage = random.randint(1, player.attack)    # Randomize player's damage
        monster.health -= player.damage # Monster takes damage
        monster.damage = random.randint(1, monster.attack)  # Randomize monster's damage
        player.health -= monster.damage # Player takes damage

        # Display player and monster attacks
        game.game_text.append(format_output(f"The {monster.name} attacks you!"))    # Display monster's attack
        game.game_text.append(format_output(f"You deal {player.damage} damage to the {monster.name}.\nThe {monster.name} deals {monster.damage} damage to you."))
        game.render_screen(monster)  # Render screen after monster's turn

        if monster.health <= 0:
            game.game_text.append(format_output(f"You have defeated the {monster.name}!"))
            game.render_screen(monster)
            break
        if player.health <= 0:
            game.game_text.append(format_output("You have been defeated!"))
            game.render_screen(monster)
            break

        prompt_continue()