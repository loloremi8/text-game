class Room:
    def __init__(self, description, actions=None, exits=None):
        self.description = description
        self.actions = actions if actions is not None else {}
        self.exits = exits if exits is not None else {}

    def add_action(self, action_name, action_function):
        self.actions[action_name] = action_function

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def describe(self):
        return self.description

    def get_actions(self):
        return self.actions.keys()

    def get_exits(self):
        return self.exits.keys()