import random
from monsters import normal_monsters, special_monsters

class Room:
    def __init__(self, description, actions, monsters=None):
        self.description = description
        self.actions = actions
        self.monsters = monsters if monsters else []

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
        {"Go forward": "hallway"}
    ),
    "hallway": Room(
        "You enter a long hallway with doors on either side.",
        {"Open left door": "treasure_room", "Open right door": "monster_room", "Go forward": "library"}
    ),
    "treasure_room": Room(
        "You find an empty room with only a chest in one of the dark corners of the room.",
        {"Go back": "hallway", "Move closer to the chest": "move_to_chest"}
    ),
    "monster_room": Room(
        "A fearsome monster appears!",
        {"fight": "monster_room", "Go back": "hallway"},
        [normal_monsters[random.randint(0, 2)]]
    ),
    "empty_room": Room(
        "You are now in an empty room. What do you do?",
        {"Go back": "hallway", "Explore further": "boss_room"}
    ),
    "boss_room": Room(
        "You enter a grand chamber. A powerful boss awaits!",
        {"fight": "boss_room"},
        [special_monsters[random.randint(0, 1)]]
    ),
    "library": Room(
        "You enter a quiet library filled with ancient books.",
        {"Go back": "hallway", "Search the room": "search_room"}
    )
}