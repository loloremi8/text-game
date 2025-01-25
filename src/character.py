class Character:
    def __init__(self, name="", p_class="", health=100, attack=10, defense=0):
        self.name = name
        self.p_class = p_class
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

    def display_status(self):
        """Displays the player's status and inventory on the right side."""
        stats = f"""
        Player Stats:
        -------------
        Name: {self.name}
        Class: {self.p_class}
        Health: {self.health}/{self.max_health}
        Attack: {self.attack} (+{self.equipped_weapon['effect']['attack'] if self.equipped_weapon else 0})
        Defense: {self.defense} (+{self.equipped_armor['effect']['defense'] if self.equipped_armor else 0})

        Equiped:
        Armor: {self.equipped_armor['name'] if self.equipped_armor else "None"}, Weapon: {self.equipped_weapon['name'] if self.equipped_weapon else "None"}

        Inventory:
        {', '.join([f"{item['name']} (+{item['effect']['health']} Health)" if item['type'] == 'consumable' else item['name'] for item in self.inventory]) if self.inventory else 'Empty'}
        """
        return stats

    def choose_name(self):
        """Allows the player to choose a name"""
        self.name = input("What is your name adventurer? ").strip()

    def choose_class(self):
        """Allows the player to choose a class."""
        while True:
            print("Choose your class:")
            print(" Starting stats: Health: 100, Attack: 10, Defense: 0")
            print(" [1] Warrior - Strong and durable. (+50 health; +5 attack)")
            print(" [2] Mage - Master of spells. (+Magic Wand; +5 defense)")
            print(" [3] Rogue - Quick and stealthy. (+10 attack)")
            choice = input("> ").strip()
            if choice == "1":
                self.p_class = "Warrior"
                self.health += 50
                self.max_health = self.health
                self.attack += 5
                break
            elif choice == "2":
                self.p_class = "Mage"
                self.inventory.append({"name": "Magic Wand", "type": "weapon", "effect": {"attack": 5}})
                self.defense += 5
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
                    self.health = min(self.max_health, self.health + item["effect"]["health"])
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and gained {item['effect']['health']} health.")
                elif item["type"] == "weapon":
                    self.equip_weapon(item)
                elif item["type"] == "armor":
                    self.equip_armor(item)
                return
        print("Item not found in inventory.")

    def equip_weapon(self, weapon):
        """Equips a weapon."""
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        self.attack += weapon["effect"]["attack"]
        self.inventory.remove(weapon)
        print(f"You equipped {weapon['name']} and gained {weapon['effect']['attack']} attack.")

    def equip_armor(self, armor):
        """Equips armor."""
        if self.equipped_armor:
            self.inventory.append(self.equipped_armor)
        self.equipped_armor = armor
        self.defense += armor["effect"]["defense"]
        self.inventory.remove(armor)
        print(f"You equipped {armor['name']} and gained {armor['effect']['defense']} defense.")