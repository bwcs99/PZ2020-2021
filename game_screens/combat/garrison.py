from game_screens.units import Unit

# a concept for test purposes, feel free to change or add more
""" Dictionary of soldiers' properties. """
SOLDIER_PROPS = [
    {'type': 'Poor Infantry', 'health': 5, 'damage': 20, 'probability': 0.4},
    {'type': 'Archers', 'health': 15, 'damage': 5, 'probability': 0.8},
    {'type': 'Cavalry', 'health': 10, 'damage': 10, 'probability': 0.6},
    {'type': 'DUCK', 'health': 1, 'damage': 1, 'probability': 0.15},
    {'type': 'PANZERKAMPFWAGEN VI TIGER', 'health': 500, 'damage': 500, 'probability': 0.5},
]


class Garrison(Unit):
    """ Unit inheritance that represents a group of soldiers. """

    def __init__(self, tile, owner, soldier_stats, count):
        super().__init__(tile, owner)
        self.type = soldier_stats['type']
        self.damage = soldier_stats['damage']
        self.health = soldier_stats['health'] * count
        self.probability = soldier_stats['probability']
        self.count = count
        # super().__init__(tile, owner)  # TODO uncomment when done testing
