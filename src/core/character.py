from combat import magic
from utils.helpers import clear_screen

class Character:
    def __init__(self):
        self.name = ""
        self.p_class = ""
        self.health = 100
        self.max_health = 100
        self.mana = 0
        self.max_mana = 0
        self.attack = 10
        self.defense = 5
        self.base_attack = 10
        self.base_defense = 5
        self.crit_chance = 0
        self.inventory = []
        self.spells = []
        self.equipped = {
            "weapon": None,
            "helmet": None,
            "chestplate": None,
            "shield": None,
            "boots": None
        }

    def choose_name(self):
        """Allows the player to choose a name."""
        while True:
            name = input("Enter your character's name: ").strip()
            if name:
                self.name = name
                break
            else:
                print("Please enter a valid name.")

    def choose_class(self):
        """Allows the player to choose a class."""
        classes = {
            "warrior": {
                "health": 150,
                "max_health": 150,
                "mana": 0,
                "max_mana": 0,
                "attack": 15,
                "defense": 8,
                "crit_chance": 0,
                "spells": []
            },
            "mage": {
                "health": 80,
                "max_health": 80,
                "mana": 50,
                "max_mana": 50,
                "attack": 5,
                "defense": 2,
                "crit_chance": 0,
                "spells": [magic.fireball, magic.heal]
            },
            "rogue": {
                "health": 100,
                "max_health": 100,
                "mana": 20,
                "max_mana": 20,
                "attack": 12,
                "defense": 4,
                "crit_chance": 0.25,
                "spells": []
            }
        }

        print("\nAvailable classes:")
        for cls_name, stats in classes.items():
            print(f"\n  {cls_name.capitalize()}:")
            print(f"    Health: {stats['health']}, Mana: {stats['mana']}")
            print(f"    Attack: {stats['attack']}, Defense: {stats['defense']}")
            if stats['spells']:
                spell_names = ", ".join([s.name.capitalize() for s in stats['spells']])
                print(f"    Spells: {spell_names}")
            if stats['crit_chance']:
                print(f"    Crit Chance: {int(stats['crit_chance'] * 100)}%")

        while True:
            choice = input("\nChoose your class (warrior/mage/rogue): ").strip().lower()
            if choice in classes:
                self.p_class = choice.capitalize()
                stats = classes[choice]
                self.health = stats["health"]
                self.max_health = stats["max_health"]
                self.mana = stats["mana"]
                self.max_mana = stats["max_mana"]
                self.attack = stats["attack"]
                self.defense = stats["defense"]
                self.base_attack = stats["attack"]
                self.base_defense = stats["defense"]
                self.crit_chance = stats["crit_chance"]
                self.spells = list(stats["spells"])
                print(f"\nYou chose the {self.p_class} class!")
                break
            else:
                print("Invalid class. Please choose warrior, mage, or rogue.")

    def display_status(self):
        """Returns the player's status as a formatted string."""
        weapon_name = self.equipped["weapon"]["name"] if self.equipped["weapon"] else "None"
        helmet_name = self.equipped["helmet"]["name"] if self.equipped["helmet"] else "None"
        chestplate_name = self.equipped["chestplate"]["name"] if self.equipped["chestplate"] else "None"
        shield_name = self.equipped["shield"]["name"] if self.equipped["shield"] else "None"
        boots_name = self.equipped["boots"]["name"] if self.equipped["boots"] else "None"
        stats = f"""Player Stats:
--------------
Name: {self.name}
Class: {self.p_class}
Health: {self.health}/{self.max_health}
Mana: {self.mana}/{self.max_mana}
Attack: {self.attack}
Defense: {self.defense}
Weapon: {weapon_name}
Helmet: {helmet_name}
Chestplate: {chestplate_name}
Shield: {shield_name}
Boots: {boots_name}"""
        if self.crit_chance > 0:
            stats += f"\nCrit Chance: {int(self.crit_chance * 100)}%"
        return stats

    def use_item(self, item_name):
        """Uses an item from the inventory."""
        item = None
        for i in self.inventory:
            if i["name"].lower() == item_name.lower():
                item = i
                break

        if not item:
            print(f"  You don't have '{item_name}' in your inventory.")
            return False

        if item["type"] == "consumable_health":
            heal_amount = item["effect"]["health"]
            old_health = self.health
            self.health = min(self.health + heal_amount, self.max_health)
            actual_heal = self.health - old_health
            print(f"  You used {item['name']} and restored {actual_heal} health. (Health: {self.health}/{self.max_health})")
            self.inventory.remove(item)
            return True

        elif item["type"] == "consumable_mana":
            mana_amount = item["effect"]["mana"]
            old_mana = self.mana
            self.mana = min(self.mana + mana_amount, self.max_mana)
            actual_mana = self.mana - old_mana
            print(f"  You used {item['name']} and restored {actual_mana} mana. (Mana: {self.mana}/{self.max_mana})")
            self.inventory.remove(item)
            return True

        elif item["type"] == "consumable_health_capacity":
            capacity = item["effect"]["health_capacity"]
            self.max_health += capacity
            self.health += capacity
            print(f"  You used {item['name']}! Max health increased by {capacity}. (Health: {self.health}/{self.max_health})")
            self.inventory.remove(item)
            return True

        elif item["type"] == "consumable_mana_capacity":
            capacity = item["effect"]["mana_capacity"]
            self.max_mana += capacity
            self.mana += capacity
            print(f"  You used {item['name']}! Max mana increased by {capacity}. (Mana: {self.mana}/{self.max_mana})")
            self.inventory.remove(item)
            return True

        elif item["type"] == "spell_book":
            spell = item["effect"]["spell"]
            for known_spell in self.spells:
                if known_spell.name.lower() == spell.name.lower():
                    print(f"  You already know {spell.name.capitalize()}!")
                    return False
            self.spells.append(spell)
            self.inventory.remove(item)
            return True

        elif item["type"] == "weapon":
            # Unequip current weapon first
            current_weapon = self.equipped["weapon"]
            if current_weapon:
                self.attack -= current_weapon["effect"]["attack"]
                self.inventory.append(current_weapon)
                print(f"  You unequipped {current_weapon['name']}.")

            # Equip new weapon
            self.equipped["weapon"] = item
            self.attack += item["effect"]["attack"]
            self.inventory.remove(item)
            print(f"  You equipped {item['name']}! Attack: {self.attack} (+{item['effect']['attack']})")
            return True

        elif item["type"] == "armor":
            slot = item["slot"]
            current = self.equipped[slot]
            if current:
                self.defense -= current["effect"]["defense"]
                self.inventory.append(current)
                print(f"  You unequipped {current['name']}.")

            self.equipped[slot] = item
            self.defense += item["effect"]["defense"]
            self.inventory.remove(item)
            print(f"  You equipped {item['name']} ({slot})! Defense: {self.defense} (+{item['effect']['defense']})")
            return True

        else:
            print(f"  You can't use {item['name']}.")
            return False

    def cast_spell(self, spell_name):
        """Casts a spell by name."""
        for spell in self.spells:
            if spell.name.lower() == spell_name.lower():
                if self.mana >= spell.mana_cost:
                    self.mana -= spell.mana_cost
                    if spell.spell_type == "heal":
                        heal_amount = spell.effect
                        old_health = self.health
                        self.health = min(self.health + heal_amount, self.max_health)
                        actual_heal = self.health - old_health
                        return {"type": "heal", "amount": actual_heal}
                    elif spell.spell_type == "damage":
                        return {"type": "damage", "amount": spell.effect}
                    elif spell.spell_type == "shield":
                        return {"type": "shield", "amount": spell.effect}
                else:
                    return None
        return None