import random
from combat.monsters import normal_monsters, special_monsters

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
        {"Open left door": "treasure_room", "Open right door": "monster_room", "Go forward": "library", "Go back": "start"},
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
        [random.choice(normal_monsters) for _ in range(random.randint(1, 2))],
        coordinates=(3, 3)
    ),
    "empty_room": Room(
        "You are now in an empty room. What do you do?",
        {"Go back": "hallway", "Explore further": "dining_hall"},
        coordinates=(3, 3)
    ),
    "boss_room": Room(
        "You enter a grand chamber. A powerful boss awaits!",
        {"fight": "boss_room", "Go back": "library"},
        [random.choice(special_monsters)],
        coordinates=(2, 1)
    ),
    "library": Room(
        "You enter a quiet library filled with ancient books.",
        {"Go back": "hallway", "Search the room": "search_library", "Go forward": "boss_room", "Open left door": "armory"},
        coordinates=(2, 2)
    ),
    "armory": Room(
        "You find yourself in an armory filled with weapons and armor.",
        {"Go back": "library", "Search the armory": "search_armory"},
        coordinates=(1, 2)
    ),
    "dining_hall": Room(
        "You enter a grand dining hall with a long table set for a feast.",
        {"Go back": "empty_room", "Search the dining hall": "search_dining_hall", "Explore further": "kitchen"},
        coordinates=(4, 3)
    ),
    "kitchen": Room(
        "You find yourself in a kitchen filled with delicious food.",
        {"Go back": "dining_hall", "Search the kitchen": "search_kitchen", "Explore further": "garden"},
        coordinates=(4, 2)
    ),
    "garden": Room(
        "You step into a beautiful garden filled with exotic plants.",
        {"Go back": "kitchen", "Search the garden": "search_garden", "Explore further": "fountain"},
        coordinates=(4, 1)
    ),
    "fountain": Room(
        "You find a serene fountain in the center of the garden.",
        {"Go back": "garden", "Interact with the fountain": "interaction_with_fountain"},
        coordinates=(4, 0)
    ),
    "throne_room": Room(
        "You enter a grand throne room with a majestic throne at the end.",
        {"Go back": "boss_room", "Approach the throne": "approach_throne", "Open left door": "exit"},
        coordinates=(2, 0)
    ),
    "exit": Room(
        "You find the exit of the dungeon.",
        {"Go back": "throne_room", "Leave the dungeon": "exit"},
        coordinates=(1, 0)
    )
}