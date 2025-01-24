from monsters import normal_monsters, special_monsters

class Room:
    def __init__(self, description, actions):
        self.description = description
        self.actions = actions

    def add_exit(self, direction, room):
        self.actions[direction] = room

    def describe(self):
        return self.description

    def get_actions(self):
        return list(self.actions.keys())

    def get_exits(self):
        return list(self.actions.keys())

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
        {"fight": normal_monsters[0]}  # Assign Goblin to monster_room
    )
}