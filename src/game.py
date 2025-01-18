from character import Character
from room import Room
from utils.helpers import clear_screen, validate_input, format_output

class Game:
    def __init__(self):
        self.current_room = None
        self.player = None

    def start_game(self):
        """Initializes the game and starts the main loop."""
        print("Welcome to the Text Game!")
        self.setup_game()
        while True:
            self.play_turn()

    def setup_game(self):
        """Sets up the initial game state, including rooms and characters."""
        # Initialize rooms
        room1 = Room("You are in a dark room. There is a door to the north.")
        room2 = Room("You are in a bright room. There is a door to the south.")
        room1.add_exit("north", room2)
        room2.add_exit("south", room1)

        # Initialize player
        self.player = Character("Hero", "Warrior")

        # Set initial room
        self.current_room = room1

    def play_turn(self):
        """Handles the actions for the current turn."""
        clear_screen()
        print(format_output(self.current_room.describe()))
        print("Available actions: ", ", ".join(self.current_room.get_actions()))
        print("Available exits: ", ", ".join(self.current_room.get_exits()))

        action = validate_input("What do you want to do? ", ["move", "inventory", "quit"])
        if action == "move":
            direction = validate_input("Which direction? ", self.current_room.get_exits())
            self.transition_room(self.current_room.exits[direction])
        elif action == "inventory":
            print("Inventory: ", ", ".join(self.player.show_inventory()))
        elif action == "quit":
            print("Thanks for playing!")
            exit()

    def transition_room(self, new_room):
        """Transitions the player to a new room."""
        self.current_room = new_room
        print(f"You have entered: {self.current_room.describe()}")

    def handle_event(self, event):
        """Handles game events."""
        # Logic for handling events
        pass