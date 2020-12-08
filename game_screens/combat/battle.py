import random

from .garrison import Garrison

# a concept for test purposes, feel free to change or add more
SOLDIER_PROPS = [
    {'type': 'ARCHER', 'health': 5, 'damage': 20, 'probability': 0.4},
    {'type': 'KNIGHT', 'health': 15, 'damage': 5, 'probability': 0.8},
    {'type': 'CAVALRY', 'health': 10, 'damage': 10, 'probability': 0.6},
    {'type': 'DUCK', 'health': 1, 'damage': 1, 'probability': 0.15},
    {'type': 'PANZERKAMPFWAGEN VI TIGER', 'health': 500, 'damage': 500, 'probability': 0.5},
]


def go_fighting(defender: Garrison, attacker: Garrison, seed=None) -> Garrison:
    if seed is not None:
        random.seed(seed)
    print(f"\nA battle between {defender.count} {defender.type} "
          f"and {attacker.count} {attacker.type} is about to start!")
    while defender.health > 0 and attacker.health > 0:
        if random.uniform(0, 1) < attacker.probability:
            defender.health -= attacker.damage
        if random.uniform(0, 1) < defender.probability:
            attacker.health -= defender.damage

    if attacker.health > defender.health:
        winner = attacker
    elif defender.health > attacker.health:
        winner = defender
    else:
        winner = None  # draw, both died :<

    if winner is not None:
        print(f'The winner is {winner.type}!\nWith {winner.health} total health left.')
    else:
        print('Both sides have suffered extreme damage.')

    return winner
