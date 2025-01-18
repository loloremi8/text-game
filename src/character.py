class Character:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def show_inventory(self):
        return self.inventory

    def __str__(self):
        return f"{self.name} the {self.class_type}"