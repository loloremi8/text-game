from utils.helpers import validate_input, prompt_continue, format_loot_description

def offer_loot(game, items, monster=None):
    """Offers each item to the player and returns the ones they took.

    `monster` is passed through to the renderer so that looting mid-combat
    keeps the monster panel on screen.
    """
    taken = []
    if not items:
        return []

    for loot in items:
        loot_description = format_loot_description(loot)
        game.game_text = f"You found: {loot_description}"
        game.render_screen(monster)

        take = validate_input(
            f"Take the {loot['name']}? (yes/no) > ",
            ["yes", "no"],
            {"y": "yes", "n": "no"}
        )
        if take == "yes":
            game.player.inventory.add(loot)
            taken.append(loot)
            game.game_text = f"You took the {loot['name']}!"
        else:
            game.game_text = f"You left the {loot['name']} behind."

        game.render_screen(monster)
        prompt_continue()

    return taken
