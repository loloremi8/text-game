import time
import textwrap
from character import Character
from room import Room, rooms
from monsters import Monster, normal_monsters, special_monsters
from combat import combat
from utils.helpers import clear_screen, validate_input, format_output, prompt_continue

class Game:
    def __init__(self):
        self.player = Character()
        self.rooms = rooms
        self.current_room = "start"
        self.game_text = []  # To store the history of game events

    def render_screen(self, monster=None):
        """Renders the screen with the latest message and status."""
        clear_screen()
        
        if (monster): # Display monster stats if there is a monster
            # Display the latest message
            latest_message = self.game_text[-1] if self.game_text else ""
            wrapped_text = textwrap.fill(latest_message, width=50)
        
            # Display the wrapped text, monster stats, and player stats        
            stats = self.player.display_status()
            stats_lines = stats.split("\n")

            monster_stats = monster.display_status()
            monster_stats_lines = monster_stats.split("\n")

            # Calculate the maximum number of lines for wrapping
            max_lines = max(len(wrapped_text.split("\n")), len(stats_lines), len(monster_stats_lines))

            # Padding lines if the text, monster stats, or player stats are shorter
            wrapped_text_lines = wrapped_text.split("\n")
            wrapped_text_lines += [""] * (max_lines - len(wrapped_text_lines))
            stats_lines += [""] * (max_lines - len(stats_lines))
            monster_stats_lines += [""] * (max_lines - len(monster_stats_lines))

            # Print the split screen with the latest message, monster stats, and player stats
            for left, middle, right in zip(wrapped_text_lines, monster_stats_lines, stats_lines):
                print(f"{left:<50} | {middle:<30} | {right:<30}")
        
        else:   # Display only player stats if there is no monster
            # Display the latest message
            latest_message = self.game_text[-1] if self.game_text else ""
            wrapped_text = textwrap.fill(latest_message, width=70)
        
            # Display the wrapped text, monster stats, and player stats        
            stats = self.player.display_status()
            stats_lines = stats.split("\n")

            monster_stats_lines = [""] * len(stats_lines)

            # Calculate the maximum number of lines for wrapping
            max_lines = max(len(wrapped_text.split("\n")), len(stats_lines))

            # Padding lines if the text or stats are shorter
            wrapped_text_lines = wrapped_text.split("\n")
            wrapped_text_lines += [""] * (max_lines - len(wrapped_text_lines))
            stats_lines += [""] * (max_lines - len(stats_lines))

            # Print the split screen with the latest message and status
            for left, right in zip(wrapped_text_lines, stats_lines):
                print(f"{left:<75} | {right}")

        # Add the separator line
        print("-" * 120)

    def show_actions(self, room):
        """Show available actions for the current room."""
        print("\nAvailable Actions:")
        for i, action in enumerate(room.actions.keys(), 1):
            print(f" [{i}] {action}")
        print(" [0] Quit")

    def get_action(self, room):
        """Prompts the player to choose an action."""
        self.show_actions(room)
        while True:
            try:
                choice = input(f"\nWhat do you do? > ").strip().lower() 
                if choice == "0":
                    print("You chose to quit the game.")
                    return None  # Exiting game
                action = list(room.actions.keys())[int(choice) - 1]
                return action
            except (ValueError, IndexError):
                print("Invalid choice, please try again.")

    def start_game(self):
        """Starts the game."""
        clear_screen()
        print("Welcome to the Fantasy Adventure Game!")
        self.player.choose_name()
        self.player.choose_class()
        message = format_output(f"Good luck on your journey, {self.player.name} the {self.player.p_class}!")
        self.game_text.append(message)
        self.render_screen()
        time.sleep(2)  # Add delay to display the message
        prompt_continue()  # Prompt the player to continue
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        while True:
            room = self.rooms[self.current_room]
            self.game_text.append(format_output(room.describe()))  # Append room description to game text
            self.render_screen()
            
            if not room.actions:
                self.game_text.append(format_output("Game over!"))
                self.render_screen()
                prompt_continue()  # Prompt the player to continue
                break

            action = self.get_action(room)
            if action is None:  # Player chose to quit
                break

            # Combat mechanic loop
            if action in room.actions:
                next_room = room.actions[action]
                if next_room == "monster_room":
                    if room.monsters:
                        monsters = room.monsters
                        if not combat(self, self.player, monsters):
                            break  # Player ran away
                        room.monsters = []  # Clear monsters after combat
                        room.update_description("You are now in an empty room. What do you do?")
                    else:
                        self.game_text.append(format_output("The room is empty."))
                self.current_room = next_room
                self.game_text.append(format_output(f"You move to the {self.current_room} room."))
            else:
                self.game_text.append(format_output("You can't do that."))
            
            self.render_screen()

    def manage_inventory(self):
        """Manages the player's inventory."""
        while True:
            clear_screen()
            print("Inventory:")
            for i, item in enumerate(self.player.inventory, 1):
                print(f" [{i}] {item['name']}")
            print(" [0] Back")

            choice = input("\nWhat do you want to do? > ").strip().lower()
            if choice == "0":
                break
            try:
                item = self.player.inventory[int(choice) - 1]
                self.player.use_item(item["name"])
                prompt_continue()
            except (ValueError, IndexError):
                print("Invalid choice, please try again.")
                prompt_continue()