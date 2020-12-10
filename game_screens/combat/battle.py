import random

from .garrison import Garrison


def go_fighting(defender: Garrison, attacker: Garrison, seed=None) -> Garrison:
    """ Begins a battle between 2 garrisons.
        Returns the winner or None if the clash ended in a draw."""
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
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
