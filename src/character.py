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
        Attack: {self.attack}

        Inventory:
        {', '.join(self.inventory) if self.inventory else 'Empty'}
        """
        return stats

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
                self.inventory.append("Magic Wand")
                break
            elif choice == "3":
                self.p_class = "Rogue"
                self.attack += 10
                break
            else:
                print("Invalid choice, please select 1, 2, or 3.")