from game_screens.units import Unit

# a concept for test purposes, feel free to change or add more
""" Dictionary of soldiers' properties. """
SOLDIER_PROPS = [
    {'type': 'ARCHER', 'health': 5, 'damage': 20, 'probability': 0.4, 'max_movement': 5},
    {'type': 'KNIGHT', 'health': 15, 'damage': 5, 'probability': 0.8, 'max_movement': 2},
    {'type': 'CAVALRY', 'health': 10, 'damage': 10, 'probability': 0.6, 'max_movement': 15},
    {'type': 'DUCK', 'health': 1, 'damage': 1, 'probability': 0.15, 'max_movement': 1},
    {'type': 'PANZERKAMPFWAGEN VI TIGER', 'health': 500, 'damage': 500, 'probability': 0.5, 'max_movement': 50}
]


class Garrison(Unit):
    """ Unit inheritance that represents a group of soldiers. """

    def __init__(self, tile, owner, soldier_stats, count):
        self.type = soldier_stats['type']
        self.damage = soldier_stats['damage']
        self.health = soldier_stats['health'] * count
        self.probability = soldier_stats['probability']
        self.count = count
        self.max_movement = self.movement = soldier_stats['max_movement']
        super().__init__(tile, owner)  # TODO uncomment when done testing
