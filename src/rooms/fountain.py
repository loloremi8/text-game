import random
from utils.helpers import validate_input, prompt_continue

def handle_fountain_interaction(game):
    """Handles the interaction with the fountain."""
    if game.fountain_interactions >= 3:
        game.game_text = "The fountain's magic seems to have faded. You can't interact with it anymore."
        game.render_screen()
        prompt_continue()
        return

    game.game_text = "You approach the fountain and see its clear, sparkling water."
    game.render_screen()
    action = validate_input("Do you want to throw a coin into the fountain or drink the water? (throw/drink/leave) > ", ["throw", "drink", "leave"])
    
    if action == "throw":
        game.game_text = "You throw a coin into the fountain and make a wish."
        game.render_screen()
        reward = random.choice(["health", "mana", "item"])
        if reward == "health":
            game.player.health = min(game.player.max_health, game.player.health + 20)
            game.game_text = "You feel a surge of vitality. Your health has increased by 20."
        elif reward == "mana":
            game.player.mana = min(game.player.max_mana, game.player.mana + 20)
            game.game_text = "You feel a surge of magical energy. Your mana has increased by 20."
        elif reward == "item":
            item = {"name": "Mystic Amulet", "type": "armor", "slot": "helmet", "effect": {"defense": 5}, "rarity": "rare"}
            game.player.inventory.append(item)
            game.game_text = "You find a Mystic Amulet in the fountain."
        game.render_screen()
    elif action == "drink":
        game.game_text = "You drink the water from the fountain."
        game.render_screen()
        game.player.health = min(game.player.max_health, game.player.health + 30)
        game.player.mana = min(game.player.max_mana, game.player.mana + 30)
        game.game_text = "You feel rejuvenated. Your health and mana have increased by 30."
        game.render_screen()
    else:
        game.game_text = "You decide to leave the fountain."
        game.render_screen()

    game.fountain_interactions += 1
    prompt_continue()