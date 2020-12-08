from game_screens.units import Unit


class Garrison(Unit):
    def __init__(self, tile, owner, soldier_stats, count):
        self.type = soldier_stats['type']
        self.damage = soldier_stats['damage']
        self.health = soldier_stats['health'] * count
        self.probability = soldier_stats['probability']
        self.count = count
        # super().__init__(tile, owner)  # TODO uncomment when done testing
