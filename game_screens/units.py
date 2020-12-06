import arcade

from game_screens.city import City
from game_screens.tiles import Tile


class Unit(arcade.sprite.Sprite):
    def __init__(self, color, tile):
        super().__init__(":resources:images/enemies/saw.png")
        self.color = color
        self.tile = tile
        self.width = tile.width
        self.height = tile.height
        self.owner = "me"
        self.health = 100
        self.max_movement = self.movement = 5
        self.move_to(tile, 0)

    def __str__(self):
        return f"{self.owner}'s {type(self).__name__}"

    def move_to(self, tile: Tile, cost: int):
        """
        Moves a unit to the specified tile at a specified cost.
        :param tile: tile to move the unit to
        :param cost: the cost of the move
        """
        self.tile.occupant = None
        self.tile = tile
        self.tile.occupant = self
        self.center_x = tile.center_x
        self.center_y = tile.center_y
        self.movement -= cost

    def reset_movement(self):
        self.movement = self.max_movement


class Settler(Unit):
    def build_city(self):
        self.tile.occupant = None
        return City(self)