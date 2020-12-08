from math import inf

import arcade

TILE_COLORS = [
            (0, 64, 128),    # water
            (112, 169, 0),   # plains
            (16, 128, 64),   # hills
            (128, 128, 128)  # mountains
        ]


class Tile(arcade.SpriteSolidColor):
    """
    Represents a single square map tile. Has the ability to hold information about the potential unit occupying it.
    """

    def __init__(self, x, y, size: int, cost: int):
        super().__init__(size, size, TILE_COLORS[cost])
        self.coords = x, y
        self.occupant = None
        self.city = None
        self.owner = None
        self.cost = cost if 0 < cost < 3 else inf
        self.type = cost  # variable to determine what kind of tile it is.

    def __repr__(self):
        return str(self.coords)

    def occupied(self):
        return bool(self.occupant)

    def set_owner(self, new_owner):
        self.owner = new_owner
        #self.color = new_owner.color


class BlinkingTile(arcade.SpriteSolidColor):
    """ An animated blinking rectangle used to illustrate a unit's move range. """
    def __init__(self, tile):
        super().__init__(tile.width, tile.height, arcade.color.WHITE)
        self.center_x = tile.center_x
        self.center_y = tile.center_y
        self.alpha = 0
        self.alpha_change = -10

    def update(self):
        if self.alpha == 150 or self.alpha == 0:
            self.alpha_change = -self.alpha_change
        self.alpha += self.alpha_change


class BorderTile(arcade.Sprite):
    def __init__(self, tile, angle):
        super().__init__("resources/sprites/border.png")
        self.width = tile.width
        self.height = tile.height
        self.center_x = tile.center_x
        self.center_y = tile.center_y
        self.angle = angle
        self.color = tile.owner.color
