class Character:
    def __init__(self, name="", player_class="", health=100, attack=10):
        self.name = name
        self.player_class = player_class
        self.health = health
        self.attack = attack
        self.inventory = []

    def display_status(self):
        # Displays the player's status and inventory on the right side
        stats = f"""
        Player Stats:
        -------------
        Name: {self.name}
        Class: {self.player_class}
        Health: {self.health}
        Attack: {self.attack}

        Inventory:
        {', '.join(self.inventory) if self.inventory else 'Empty'}
        """
        return stats