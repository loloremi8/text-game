def clear_screen():
    """Clears the console screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_input(prompt, valid_options):
    """Prompts the user for input and validates it against valid options."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print("Invalid choice, please try again.")

def format_output(text):
    """Formats output text for better readability."""
    return f"\n{text}\n"

def prompt_continue():
    """Prompts the player to press Enter to continue."""
    input("\nPress Enter to continue...")