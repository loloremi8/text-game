import time
import textwrap
from character import Character
from room import rooms
from combat import combat
from loot import generate_treasure_chest_loot, generate_library_loot
from magic import fireball, heal, lightning, ice_blast, shield
from utils.helpers import clear_screen, validate_input, format_output, prompt_continue

class Game:
    def __init__(self):
        self.player = Character()
        self.rooms = rooms
        self.current_room = "start"
        self.game_text = []  # To store the history of game events
        self.treasure_room_looted = False
        self.library_looted = False

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
        print(" [i] Inventory")
        print(" [0] Quit Game")

    def get_action(self, room):
        """Prompts the player to choose an action."""
        self.show_actions(room)
        while True:
            choice = input(f"\nWhat do you do? > ").strip().lower()
            if choice == "0":
                print("You chose to quit the game.")
                return None  # Exiting game
            elif choice == "i":
                self.manage_inventory()
                self.render_screen()
                self.show_actions(room)
            else:
                try:
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

            # Handle treasure room interactions
            if self.current_room == "treasure_room" and action == "Move closer to the chest":
                if not self.treasure_room_looted:
                    move_to_chest = validate_input(f"Do you want to open the chest? (yes/no) > ", ["yes", "no"])
                    if move_to_chest == "yes":
                        loot_items = generate_treasure_chest_loot()
                        for loot in loot_items:
                            if loot["type"].startswith("consumable"):
                                effect_type = list(loot["effect"].keys())[0]
                                loot_description = f"{loot['name']} (+{loot['effect'][effect_type]} {effect_type.capitalize()})"
                            else:
                                loot_description = f"{loot['name']} ({', '.join([f'{k}: {v}' for k, v in loot['effect'].items()])})"
                            self.game_text.append(format_output(f"You found {loot_description}"))
                            take_loot = validate_input(f"Do you want to take the {loot_description}? (yes/no) > ", ["yes", "no"])
                            if take_loot == "yes":
                                self.player.inventory.append(loot)
                                self.game_text.append(format_output(f"You took the {loot['name']}!"))
                            else:
                                self.game_text.append(format_output(f"You left the {loot['name']} behind."))
                        self.treasure_room_looted = True
                    else:
                        self.game_text.append(format_output(f"You left the chest unopened."))
                else:
                    self.game_text.append(format_output(f"The chest is empty."))
                self.render_screen()
                prompt_continue()
                continue

            # Special action for the library room
            if self.current_room == "library" and action == "Search the room":
                if not self.library_looted:
                    self.handle_library_loot()
                else:
                    self.game_text.append(format_output(f"The library has been thoroughly searched."))
                self.render_screen()
                prompt_continue()
                continue

            # Combat mechanic loop
            if action in room.actions:
                next_room = room.actions[action]
                if next_room == "monster_room":
                    if room.monsters:
                        monsters = room.monsters
                        room.actions.update({"Go back": "hallway"})  # Add option to go back to hallway
                        if not combat(self, self.player, monsters):
                            continue  # Player ran away, stay in the same room
                        room.monsters = []
                        room.update_description("You are now in an empty room. What do you do?")
                        room.actions.update({"Go back": "hallway", "Explore further": "another_room"})
                    else:
                        self.game_text.append(format_output("The room is empty."))
                self.current_room = next_room
                self.game_text.append(format_output(f"You move to the {self.current_room} room."))
            else:
                self.game_text.append(format_output("You can't do that."))
            
            self.render_screen()

    def handle_library_loot(self):
        loot_items = generate_library_loot(self.player)
        for loot in loot_items:
            self.process_loot(loot)
        self.library_looted = True

    def process_loot(self, loot):
        # Telling the player that he learned a new spell 
        if loot["type"] == "consumable_spell":
            spell_name = loot["effect"]["spell"]
            spell = next(spell for spell in [fireball, heal, lightning, ice_blast, shield] if spell.name == spell_name)
            self.player.spells.append(spell)
            print(f"You read through the old books and grimmoires and you learned a new spell: {spell_name}!")
            prompt_continue()
        elif loot["type"] == "consumable_mana_capacity":
            take_loot = validate_input(f"Do you want to take the {loot['name']} (+{loot['effect']['mana_capacity']} Mana Capacity)? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                self.player.inventory.append(loot)
            else:
                pass
        elif loot["type"] == "consumable_health_capacity":
            take_loot = validate_input(f"Do you want to take {loot['name']} (+{loot['effect']['health_capacity']} Health Capacity)? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                self.player.inventory.append(loot)
            else:
                pass
        else:
            effect_type = list(loot["effect"].keys())[0]
            effect_value = loot["effect"][effect_type]
            take_loot = validate_input(f"Do you want to take the {loot['name']} (+{effect_value} {effect_type.replace('_', ' ').capitalize()})? (yes/no) > ", ["yes", "no"])
            if take_loot == "yes":
                self.player.inventory.append(loot)
            else:
                pass

    def manage_inventory(self):
        """Manages the player's inventory."""
        while True:
            clear_screen()
            print("Inventory:")
            for i, item in enumerate(self.player.inventory, 1):
                if item["type"].startswith("consumable"):
                    effect_type = list(item["effect"].keys())[0]
                    print(f" [{i}] {item['name']} (+{item['effect'][effect_type]} {effect_type.replace('_', ' ').capitalize()})")
                else:
                    print(f" [{i}] {item['name']}")
            print(" [0] Back")
            print(" [t] Trash an item")

            choice = input("\nWhat do you want to do? > ").strip().lower()
            if choice == "0":
                break
            elif choice == "t":
                self.trash_item()
            else:
                try:
                    item = self.player.inventory[int(choice) - 1]
                    self.player.use_item(item["name"])
                    prompt_continue()
                except (ValueError, IndexError):
                    print("Invalid choice, please try again.")
                    prompt_continue()

    def trash_item(self):
        """Allows the player to trash an item from the inventory."""
        while True:
            clear_screen()
            print("Trash an item:")
            for i, item in enumerate(self.player.inventory, 1):
                if item["type"].startswith("consumable"):
                    effect_type = list(item["effect"].keys())[0]
                    print(f" [{i}] {item['name']} (+{item['effect'][effect_type]} {effect_type.capitalize()})")
                else:
                    print(f" [{i}] {item['name']}")
            print(" [0] Back")

            choice = input("\nWhich item do you want to trash? > ").strip().lower()
            if choice == "0":
                break
            try:
                item = self.player.inventory.pop(int(choice) - 1)
                print(f"You trashed {item['name']}.")
                prompt_continue()
                break
            except (ValueError, IndexError):
                print("Invalid choice, please try again.")
                prompt_continue()