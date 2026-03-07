import time
import shutil
import textwrap
from core import character
from combat.combat import combat as run_combat
from utils.helpers import clear_screen, format_output, prompt_continue, format_loot_description
from rooms.room import rooms
from rooms.treasure_room import handle_treasure_room
from rooms.library import handle_library_loot
from rooms.armory import handle_armory_loot
from rooms.kitchen import handle_kitchen_loot
from rooms.throne_room import handle_throne_room
from rooms.dining_hall import handle_dining_hall_loot
from rooms.garden import handle_garden_loot
from rooms.fountain import handle_fountain_interaction
from core import inventory

def get_terminal_width():
    """Returns the current terminal width."""
    return shutil.get_terminal_size((80, 24)).columns

class Game:
    def __init__(self):
        self.player = character.Character()
        self.rooms = rooms
        self.current_room = "start"
        self.game_text = ""  # instead of []
        self.treasure_room_looted = False
        self.library_looted = False
        self.kitchen_looted = False
        self.dining_hall_looted = False
        self.garden_looted = False
        self.armory_looted = False
        self.fountain_interactions = 0
        self.boss_room_cleared = False   # For the boss_room (Dark Knight/Lich)
        self.dragon_defeated = False      # For the throne_room (Dragon)

    def render_map(self):
        """Renders the map in the terminal."""
        map_width = 5
        map_height = 5
        map_grid = [[" " for _ in range(map_width)] for _ in range(map_height)]

        for room_name, room in self.rooms.items():
            if room.coordinates:
                x, y = room.coordinates
                if 0 <= y < map_height and 0 <= x < map_width:
                    map_grid[y][x] = "R"

        current_room = self.rooms[self.current_room]
        if current_room.coordinates:
            x, y = current_room.coordinates
            if 0 <= y < map_height and 0 <= x < map_width:
                map_grid[y][x] = "P"

        print("Map:")
        for row in map_grid:
            row_str = ""
            for cell in row:
                if cell == "R":
                    row_str += "[ ]"
                elif cell == "P":
                    row_str += "[P]"
                else:
                    row_str += " . "
            print(row_str)
        print()

    def render_screen(self, monster=None):
        """Renders the screen with the latest message and status, adapting to terminal width."""
        clear_screen()
        term_width = get_terminal_width()
        separator = "─" * term_width

        if monster:
            col_count = 3
            divider_space = 6
            usable = term_width - divider_space
            col_width = max(20, usable // col_count)

            text_width = col_width
            monster_width = col_width
            player_width = usable - text_width - monster_width

            latest_message = self.game_text if self.game_text else ""
            wrapped_text_lines = textwrap.fill(latest_message, width=text_width).split("\n")

            stats_lines = self.player.display_status().split("\n")
            monster_stats_lines = monster.display_status().split("\n")

            max_lines = max(len(wrapped_text_lines), len(stats_lines), len(monster_stats_lines))
            wrapped_text_lines += [""] * (max_lines - len(wrapped_text_lines))
            stats_lines += [""] * (max_lines - len(stats_lines))
            monster_stats_lines += [""] * (max_lines - len(monster_stats_lines))

            for left, middle, right in zip(wrapped_text_lines, monster_stats_lines, stats_lines):
                print(f"{left:<{text_width}} │ {middle:<{monster_width}} │ {right:<{player_width}}")
        else:
            divider_space = 3
            usable = term_width - divider_space
            text_width = max(20, int(usable * 0.65))
            stats_width = usable - text_width

            latest_message = self.game_text if self.game_text else ""
            wrapped_text_lines = textwrap.fill(latest_message, width=text_width).split("\n")

            stats_lines = self.player.display_status().split("\n")

            max_lines = max(len(wrapped_text_lines), len(stats_lines))
            wrapped_text_lines += [""] * (max_lines - len(wrapped_text_lines))
            stats_lines += [""] * (max_lines - len(stats_lines))

            for left, right in zip(wrapped_text_lines, stats_lines):
                print(f"{left:<{text_width}} │ {right}")

        print(separator)
        self.render_map()
        print(separator)

    def show_actions(self, room):
        """Show available actions for the current room."""
        print("\nAvailable Actions:")
        for i, action in enumerate(room.actions.keys(), 1):
            print(f"  [{i}] {action}")
        print("  [i] Inventory")
        print("  [0] Quit Game")

    def get_action(self, room):
        """Prompts the player to choose an action."""
        self.show_actions(room)
        while True:
            choice = input("\nWhat do you do? > ").strip().lower()
            if choice == "0":
                print("You chose to quit the game.")
                return None
            elif choice == "i":
                self.manage_inventory()
                self.render_screen()
                self.show_actions(room)
                continue
            else:
                try:
                    idx = int(choice) - 1
                    actions = list(room.actions.keys())
                    if 0 <= idx < len(actions):
                        return actions[idx]
                    else:
                        print("Invalid choice, please try again.")
                except ValueError:
                    print("Invalid choice, please try again.")

    def start_game(self):
        """Starts the game."""
        clear_screen()
        print("Welcome to the Dungeon crawling game!")
        self.player.choose_name()
        self.player.choose_class()
        message = format_output(f"Good luck on your journey, {self.player.name} the {self.player.p_class}!")
        self.game_text = message
        self.render_screen()
        time.sleep(2)
        prompt_continue()
        self.game_loop()

    def game_loop(self):
        """Main game loop."""
        while True:
            room = self.rooms[self.current_room]
            self.game_text = format_output(room.describe())
            self.render_screen()

            if not room.actions:
                self.game_text = format_output("Game over!")
                self.render_screen()
                prompt_continue()
                break

            action = self.get_action(room)
            if action is None:
                break

            # Handle treasure room interaction
            if self.current_room == "treasure_room" and action == "Move closer to the chest":
                handle_treasure_room(self)
                continue

            # Handle library search
            if self.current_room == "library" and action == "Search the room":
                if not self.library_looted:
                    handle_library_loot(self)
                else:
                    self.game_text = format_output("You've already searched the library.")
                    self.render_screen()
                    prompt_continue()
                continue

            # Handle armory search
            if self.current_room == "armory" and action == "Search the armory":
                handle_armory_loot(self)
                continue

            # Handle kitchen search
            if self.current_room == "kitchen" and action == "Search the kitchen":
                handle_kitchen_loot(self)
                continue

            # Handle dining hall search
            if self.current_room == "dining_hall" and action == "Search the dining hall":
                handle_dining_hall_loot(self)
                continue

            # Handle garden search
            if self.current_room == "garden" and action == "Search the garden":
                handle_garden_loot(self)
                continue

            # Handle fountain interaction
            if self.current_room == "fountain" and action == "Interact with the fountain":
                handle_fountain_interaction(self)
                continue

            # Handle throne room interaction
            if self.current_room == "throne_room" and action == "Approach the throne":
                handle_throne_room(self)
                continue

            # Handle exit / winning the game
            if self.current_room == "exit" and action == "Leave the dungeon":
                if not self.dragon_defeated:
                    self.game_text = format_output("The exit is blocked by a magical barrier. You must defeat the Dragon first!")
                    self.render_screen()
                    prompt_continue()
                    self.current_room = "throne_room"
                    continue
                else:
                    self.game_text = format_output(f"Congratulations {self.player.name}! You have escaped the dungeon and defeated the Dragon! You win!")
                    self.render_screen()
                    prompt_continue()
                    break

            # Navigate to next room
            if action in room.actions:
                next_room = room.actions[action]

                # Monster room combat
                if next_room == "monster_room" or self.current_room == "monster_room":
                    target_room = self.rooms.get("monster_room", room)
                    if target_room.monsters:
                        self.current_room = "monster_room"
                        result = run_combat(self, self.player, target_room.monsters)
                        if self.player.health <= 0:
                            self.game_text = format_output("Your journey ends here...")
                            self.render_screen()
                            prompt_continue()
                            return
                        if not result:
                            self.current_room = "hallway"
                            continue
                        target_room.monsters = []
                        target_room.update_description("You are now in an empty room. What do you do?")
                        target_room.actions = {"Go back": "hallway", "Explore further": "dining_hall"}
                        self.current_room = "monster_room"
                        continue
                    else:
                        self.current_room = next_room
                        continue

                # Boss room combat
                if next_room == "boss_room":
                    boss_room = self.rooms["boss_room"]
                    self.current_room = "boss_room"
                    if boss_room.monsters and not self.boss_room_cleared:
                        result = run_combat(self, self.player, boss_room.monsters)
                        if self.player.health <= 0:
                            self.game_text = format_output("Your journey ends here...")
                            self.render_screen()
                            prompt_continue()
                            return
                        if not result:
                            self.current_room = "library"
                            continue
                        self.boss_room_cleared = True
                        boss_room.monsters = []
                        boss_room.update_description("The grand chamber is now quiet. The boss has been defeated.")
                        boss_room.actions = {"Go back": "library", "Go forward": "throne_room"}
                        continue
                    else:
                        continue

                # Normal room transition
                self.current_room = next_room

            self.render_screen()

    def manage_inventory(self):
        """Manages the player's inventory, equipment, and spells."""
        inventory.manage_inventory(self)