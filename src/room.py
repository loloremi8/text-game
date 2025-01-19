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