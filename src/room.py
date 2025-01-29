import random
from monsters import normal_monsters, special_monsters

class Room:
    def __init__(self, description, actions, monsters=None, coordinates=None):
        self.description = description
        self.actions = actions
        self.monsters = monsters if monsters else []
        self.coordinates = coordinates  # Add coordinates to the Room class

    def add_exit(self, direction, room):
        self.actions[direction] = room

    def describe(self):
        return self.description

    def get_actions(self):
        return list(self.actions.keys())

    def get_exits(self):
        return list(self.actions.keys())

    def update_description(self, new_description):
        """Updates the room description."""
        self.description = new_description

rooms = {
    "start": Room(
        "You find yourself in a dimly lit cave. A path leads forward.",
        {"Go forward": "hallway"},
        coordinates=(2, 4)
    ),
    "hallway": Room(
        "You enter a long hallway with doors on either side.",
        {"Open left door": "treasure_room", "Open right door": "monster_room", "Go forward": "library"},
        coordinates=(2, 3)
    ),
    "treasure_room": Room(
        "You find an empty room with only a chest in one of the dark corners of the room.",
        {"Go back": "hallway", "Move closer to the chest": "move_to_chest"},
        coordinates=(1, 3)
    ),
    "monster_room": Room(
        "A fearsome monster appears!",
        {"fight": "monster_room", "Go back": "hallway"},
        [normal_monsters[random.randint(0, 2)]],
        coordinates=(3, 3)
    ),
    "empty_room": Room(
        "You are now in an empty room. What do you do?",
        {"Go back": "hallway", "Explore further": "boss_room"}
    ),
    "boss_room": Room(
        "You enter a grand chamber. A powerful boss awaits!",
        {"fight": "boss_room"},
        [special_monsters[random.randint(0, 1)]],
        coordinates=(4, 3)
    ),
    "library": Room(
        "You enter a quiet library filled with ancient books.",
        {"Go back": "hallway", "Search the room": "search_library"},
        coordinates=(2, 2)
    )
}