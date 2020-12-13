import random

from game_screens.units import Unit

# a concept for test purposes, feel free to change or add more
""" Dictionary of soldiers' properties. """
SOLDIER_PROPS = {
    'Poor Infantry': {'health': 15, 'damage': 5, 'probability': 0.8, 'max_movement': 2},
    'Archers': {'health': 5, 'damage': 20, 'probability': 0.4, 'max_movement': 3},
    'Cavalry': {'health': 10, 'damage': 10, 'probability': 0.6, 'max_movement': 4}
}


class Garrison(Unit):
    """ Unit inheritance that represents a group of soldiers. """

    def __init__(self, tile, owner, soldier_type, count):
        if tile is not None:
            super().__init__(tile, owner)
        soldier_stats = SOLDIER_PROPS[soldier_type]
        self.type = soldier_type
        self.damage = soldier_stats['damage']
        self.health = soldier_stats['health'] * count
        self.probability = soldier_stats['probability']
        self.count = count
        self.max_movement = self.movement = soldier_stats['max_movement']

    def __str__(self):
        return f"{self.owner.short_civ.capitalize()} {self.type}"

    def attack(self, defender, seed=None):
        """" Commands the garrison to attack another unit.
            Returns the winner or None if the clash ended in a draw."""
        attacker = self
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()
        print(f"\nA battle between {defender.owner}'s {defender.count} {defender.type} "
              f"and {attacker.owner}'s {attacker.count} {attacker.type} is about to start!")
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
            print(f'The winner is {winner.owner}!\nWith {winner.health} total health left.')
        else:
            print('Both sides have suffered extreme damage.')
        return winner
