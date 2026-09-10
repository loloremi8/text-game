class Spell:
    def __init__(self, name, mana_cost, spell_type, effect):
        self.name = name
        self.mana_cost = mana_cost
        self.spell_type = spell_type
        self.effect = effect

# Offensive spells
fireball = Spell("Fireball", 10, "damage", 20)
lightning = Spell("Lightning", 15, "damage", 30)
ice_blast = Spell("Ice Blast", 12, "damage", 25)

# Defensive spells
heal = Spell("Heal", 5, "heal", 15)
shield = Spell("Shield", 8, "shield", 30)