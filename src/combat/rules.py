"""Pure damage and defense rules.

These functions hold no game state so combat and tests can both call them
directly. The old formula was ``max(0, randint(1, attack) - defense)``:
because the subtraction was flat, enough defense made a combatant literally
invulnerable and every hit could sit at 0 forever, producing an unwinnable
infinite fight. Mitigation is now a percentage that approaches 1 but never
reaches it, and every hit is floored at 1 damage.
"""

import random

# How much defense it takes to reach 50% mitigation. Larger = softer defense.
DEFENSE_SOFTNESS = 12


def mitigation(defense):
    """Fraction of incoming damage that ``defense`` prevents, in [0, 1)."""
    if defense <= 0:
        return 0.0
    return defense / (defense + DEFENSE_SOFTNESS)


def melee_damage(attack, defense, crit_chance=0.0, rng=random):
    """Returns (damage, is_crit) for one melee swing.

    The raw roll stays ``randint(1, max(1, attack))`` so the existing monster
    stat scale still roughly holds; only the subtraction changed. Crits double
    the post-mitigation damage.
    """
    raw = rng.randint(1, max(1, attack))
    damage = raw * (1 - mitigation(defense))
    is_crit = crit_chance > 0 and rng.random() < crit_chance
    if is_crit:
        damage *= 2
    return max(1, int(round(damage))), is_crit


def spell_damage(amount, defense):
    """Spell damage after the target's defense mitigates it, floored at 1."""
    return max(1, int(round(amount * (1 - mitigation(defense)))))


def absorb(shield_pool, incoming):
    """Returns (remaining_pool, hp_damage) after the pool soaks what it can."""
    pool = max(0, shield_pool)
    if incoming <= 0:
        return pool, 0
    soaked = min(pool, incoming)
    return pool - soaked, incoming - soaked
