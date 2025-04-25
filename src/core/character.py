from combat.magic import fireball, heal

class Character:
    def __init__(self, name="", p_class="", health=100, attack=10, defense=0, mana=0):
        self.name = name
        self.p_class = p_class
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.max_mana = mana
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.spells = []

    def display_status(self):
        """Displays the player's status on the right side."""
        stats = f"""
        Player Stats:
        -------------
        Name: {self.name}
        Class: {self.p_class}
        Health: {self.health}/{self.max_health}
        Mana: {self.mana}/{self.max_mana}
        Attack: {self.attack} (+{self.equipped_weapon['effect']['attack'] if self.equipped_weapon else 0})
        Defense: {self.defense} (+{self.equipped_armor['effect']['defense'] if self.equipped_armor else 0})

        Equipped:
        Armor: {self.equipped_armor['name'] if self.equipped_armor else "None"}, Weapon: {self.equipped_weapon['name'] if self.equipped_weapon else "None"}
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
            print(" [2] Mage - Master of spells. (+Magic Wand; +5 defense; +50 mana)")
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
                magic_wand = {"name": "Magic Wand", "type": "weapon", "effect": {"attack": 0}}
                self.inventory.append(magic_wand)
                self.equip_weapon(magic_wand)
                self.defense += 5
                self.mana += 50
                self.max_mana = self.mana
                self.spells = [fireball, heal]
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
                if item["type"] == "consumable_health":
                    # Restores health
                    self.health = min(self.max_health, self.health + item["effect"]["health"])
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and gained {item['effect']['health']} health.")
                elif item["type"] == "consumable_mana":
                    # Restores mana
                    self.mana = min(self.max_mana, self.mana + item["effect"]["mana"])
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and gained {item['effect']['mana']} mana.")
                elif item["type"] == "consumable_mana_capacity":
                    # Increases mana capacity
                    self.max_mana += item["effect"]["mana_capacity"]
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and increased your mana capacity by {item['effect']['mana_capacity']}.")
                elif item["type"] == "consumable_health_capacity":
                    # Increases health capacity
                    self.max_health += item["effect"]["health_capacity"]
                    self.inventory.remove(item)
                    print(f"You used {item['name']} and increased your health capacity by {item['effect']['health_capacity']}.")
                elif item["type"] == "weapon":
                    self.equip_weapon(item)
                elif item["type"] == "armor":
                    self.equip_armor(item)
                return
        print("Item not found in inventory.")

    def equip_weapon(self, weapon):
        """Equips a weapon."""
        if self.equipped_weapon:
            self.attack -= self.equipped_weapon["effect"]["attack"]
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        self.attack += weapon["effect"]["attack"]
        self.inventory.remove(weapon)
        print(f"You equipped {weapon['name']} and gained {weapon['effect']['attack']} attack.")

    def equip_armor(self, armor):
        """Equips armor."""
        if self.equipped_armor:
            self.defense -= self.equipped_armor["effect"]["defense"]
            self.inventory.append(self.equipped_armor)
        self.equipped_armor = armor
        self.defense += armor["effect"]["defense"]
        self.inventory.remove(armor)
        print(f"You equipped {armor['name']} and gained {armor['effect']['defense']} defense.")

    def cast_spell(self, spell_name):
        """Casts a spell if the player has enough mana."""
        for spell in self.spells:
            if spell.name.lower() == spell_name.lower():
                return spell.cast(self)
        print("Spell not found.")
        return None