class Spell:
    def __init__(self, name, mana_cost, spell_type, effect):
        self.name = name
        self.mana_cost = mana_cost
        self.spell_type = spell_type
        self.effect = effect

    def cast(self, caster):
        if caster.mana >= self.mana_cost:
            caster.mana -= self.mana_cost
            if self.spell_type == "damage":
                return {"type": "damage", "amount": self.effect}
            elif self.spell_type == "heal":
                caster.health = min(caster.max_health, caster.health + self.effect)
                return {"type": "heal", "amount": self.effect}
        else:
            print("Not enough mana to cast the spell.")
            return None

# Offensive spells
fireball = Spell("Fireball", 10, "damage", 20)
lightning = Spell("Lightning", 15, "damage", 30)
ice_blast = Spell("Ice Blast", 12, "damage", 25)

# Defensive spells
heal = Spell("Heal", 5, "heal", 15)
shield = Spell("Shield", 5, "heal", 10)