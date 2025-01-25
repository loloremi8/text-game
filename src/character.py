class Character:
    def __init__(self, name="", p_class="", health=100, attack=10):
        self.name = name
        self.p_class = p_class
        self.health = health
        self.attack = attack
        self.inventory = []

    def display_status(self):
        """Displays the player's status and inventory on the right side."""
        stats = f"""
        Player Stats:
        -------------
        Name: {self.name}
        Class: {self.p_class}
        Health: {self.health}
        Attack: {self.attack} (+{sum([item['effect']['attack'] for item in self.inventory if item['type'] == 'weapon'])})

        Inventory:
        {', '.join([item['name'] for item in self.inventory]) if self.inventory else 'Empty'}
        """
        return stats

    def choose_name(self):
        """Allows the player to choose a name"""
        self.name = input("What is your name adventurer? ").strip()

    def choose_class(self):
        """Allows the player to choose a class."""
        while True:
            print("Choose your class:")
            print(" [1] Warrior - Strong and durable.")
            print(" [2] Mage - Master of spells.")
            print(" [3] Rogue - Quick and stealthy.")
            choice = input("> ").strip()
            if choice == "1":
                self.p_class = "Warrior"
                self.health += 50
                self.attack += 5
                break
            elif choice == "2":
                self.p_class = "Mage"
                self.inventory.append({"name": "Magic Wand", "type": "weapon", "effect": {"attack": 5}})
                break
            elif choice == "3":
                self.p_class = "Rogue"
                self.attack += 10
                break
            else:
                print("Invalid choice, please select 1, 2, or 3.")

    def use_item(self, item_name):
        """Uses an item from the inventory."""
        for item in self.inventory:
            if item["name"].lower() == item_name.lower():
                if item["type"] == "consumable":
                    self.health += item["effect"]["health"]
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and gained {item['effect']['health']} health.")
                elif item["type"] == "weapon":
                    self.attack += item["effect"]["attack"]
                    self.inventory.remove(item)
                    print(f"You equipped {item['name']} and gained {item['effect']['attack']} attack.")
                elif item["type"] == "armor":
                    self.health += item["effect"]["health"]
                    self.inventory.remove(item)
                    print(f"You equipped {item['name']} and gained {item['effect']['health']} health.")
                return
        print("Item not found in inventory.")