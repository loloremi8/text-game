import os
import textwrap
from character import Character
from room import Room

class Game:
    def __init__(self):
        self.player = Character()
        self.rooms = {
            "start": Room(
                "You find yourself in a dimly lit cave. A path leads forward.",
                {"Go forward": "hallway"}
            ),
            "hallway": Room(
                "You enter a long hallway with doors on either side.",
                {"Open left door": "treasure_room", "Open right door": "monster_room"}
            ),
            "treasure_room": Room(
                "You find a chest filled with gold. Congratulations, you win!",
                {}
            ),
            "monster_room": Room(
                "A fearsome monster appears!",
                {}
            )
        }
        self.current_room = "start" # Set initial room
        self.game_text = [] # To store game text

    def clear_screen(self):
        # Clears the terminal screen.
        os.system("cls" if os.name == "nt" else "clear")

    def render_screen(self):
        # Renders the screen with old and new messages and status.
        wrapped_text = "\n".join(self.game_text)
        wrapped_text = textwrap.fill("\n".join(self.game_text), width=70)

        # Display the wrapped text and status panel
        stats = self.player.display_status()
        stats_lines = stats.split("\n")

        # Calculate the maximum number of lines for wrapping
        max_lines = max(len(wrapped_text.split("\n")), len(stats_lines))

        # Padding lines if the text or stats are shorter
        wrapped_text_lines = wrapped_text.split("\n")
        wrapped_text_lines += [""] * (max_lines - len(wrapped_text_lines))
        stats_lines += [""] * (max_lines - len(stats_lines))

        # Print the split screen with old message first and then new
        for left, right in zip(wrapped_text_lines, stats_lines):
            print(f"{left:<75} | {right}")

    def show_actions(self, room):
        # Show available actions for the current room
        for i, action in enumerate(room.actions.keys()):
            print(f" [{i+1}] {action}")
        print(" [0] Quit")

    def get_action(self, room):
        # Prompts the player to choose an action
        self.show_actions(room)
        while True:
            try:
                choice = input(f"\nWhat do you do? > ").strip().lower()
                if choice == "0":
                    print("You chose to quit the game.")
                    return None # Exiting game
                action = list(room.actions.keys())[int(choice) - 1]
                return action
            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")

    def choose_class(self):
        # Allows the player to choose a class
        while True:
            self.clear_screen()
            print("Choose your class:")
            print(" [1] Warrior - Strong and durable.")
            print(" [2] Mage - Master of spells.")
            print(" [3] Rogue - Quick and stealthy.")
            choice = input("> ").strip()
            if choice == "1":
                self.player.player_class = "Warrior"
                self.player.health += 50
                self.player.attack += 5
                break
            elif choice == "2":
                self.player.player_class = "Mage"
                self.player.inventory.append("Magic Wand")
                break
            elif choice == "3":
                self.player.player_class = "Rogue"
                self.player.attack += 10
                break
            else:
                print("Invalid choice, please select 1, 2, or 3.")

    def start_game(self):
        # Starts the game
        self.clear_screen()
        print("Welcome to the Fantasy Adventure Game!")
        self.player.name = input("What is your name adventurer? ").strip()
        self.choose_class()
        self.game_text.append(f"Good luck oon your journey, {self.player.name} the {self.player.player_class}!")
        self.game_loop()

    def game_loop(self):
        # Main game loop
        while True:
            room = self.rooms[self.current_room]
            self.game_text.append(room.describe())  # Append room description to game text
            self.render_screen()

            # Add the separator line between old and new messages
            print("-" * 100)  # Underline separator

            if not room.actions:
                self.game_text.append("Game Over!")
                self.render_screen()
                break
            
            action = self.get_action(room)
            if action is None:  # Player chose to quit
                break

            if action in room.actions:
                self.current_room = room.actions[action]
                self.game_text.append(f"You move to the {self.current_room} room.")
            else:
                self.game_text.append("You can't do that.")

            self.render_screen()