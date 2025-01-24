import random
from utils.helpers import format_output, prompt_continue

def combat(player, monster):
    """Handles combat between the player and a monster."""
    print(format_output(f"A wild {monster.name} appears!"))
    prompt_continue()

    while player.health > 0 and monster.health > 0:
        # Display player and monster stats
        print(f"{player.display_status()} | {monster.display_status()}")

        # Player's turn
        print(format_output(f"You attack the {monster.name}!"))
        damage = random.randint(1, player.attack)
        monster.health -= damage
        print(format_output(f"You deal {damage} damage to the {monster.name}."))
        if monster.health <= 0:
            print(format_output(f"You have defeated the {monster.name}!"))
            break

        # Monster's turn
        print(format_output(f"The {monster.name} attacks you!"))
        damage = random.randint(1, monster.attack)
        player.health -= damage
        print(format_output(f"The {monster.name} deals {damage} damage to you."))
        if player.health <= 0:
            print(format_output("You have been defeated!"))
            break

        prompt_continue()