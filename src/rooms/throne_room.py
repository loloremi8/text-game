from utils.helpers import format_output, validate_input, prompt_continue

def handle_throne_room(game):
    """Handles the interaction in the throne room."""
    game.game_text.append(format_output("You approach the throne."))
    game.render_screen()
    prompt_continue()
    game.game_text.append(format_output("You find a hidden passage behind the throne leading to the exit."))
    game.render_screen()
    prompt_continue()