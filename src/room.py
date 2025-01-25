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
        {"Open left door": "treasure_room", "Open right door": "monster_room"}
    ),
    "treasure_room": Room(
        "You find a chest filled with gold. Congratulations, you win!",
        {}
    ),
    "monster_room": Room(
        "A fearsome monster appears!",
        {"fight": "monster_room"},
        [normal_monsters[random.randint(0, 2)]]
    )
}