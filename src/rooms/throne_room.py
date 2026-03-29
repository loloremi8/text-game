from utils.helpers import prompt_continue
from combat.monsters import Dragon

def handle_throne_room(game):
    """Handles the throne room boss encounter with the Dragon."""
    throne_room = game.rooms["throne_room"]
    
    if game.dragon_defeated:
        game.game_text = "The throne room is quiet. The Dragon has been slain. You can proceed to the exit."
        game.render_screen()
        prompt_continue()
        return
    
    game.game_text = "You enter the grand throne room. A massive Dragon guards the throne!"
    game.render_screen()
    prompt_continue()
    
    throne_room.monsters = [Dragon.clone()]
    
    from combat.combat import combat
    
    result = combat(game, game.player, throne_room.monsters)
    
    if game.player.health <= 0:
        game.game_text = "The Dragon has defeated you. Your journey ends here..."
        game.render_screen()
        prompt_continue()
        return
    
    if not result:
        game.game_text = "You fled from the Dragon and returned to safety."
        game.current_room = "boss_room"
        game.render_screen()
        prompt_continue()
        return
    
    game.dragon_defeated = True
    throne_room.monsters = []
    throne_room.update_description("The throne room is now quiet. The Dragon has been slain. You can proceed to the exit.")
    throne_room.actions = {"Go back": "boss_room", "Proceed to the exit": "exit"}
    
    game.game_text = "You have defeated the mighty Dragon! The path to freedom is now open!"
    game.render_screen()
    prompt_continue()