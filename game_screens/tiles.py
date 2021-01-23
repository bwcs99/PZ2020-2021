from math import inf

import arcade

TILE_TYPES = [
            "resources/sprites/tiles/water.png",        # water
            "resources/sprites/tiles/plains.png",       # plains
            "resources/sprites/tiles/hills.png",        # hills
            "resources/sprites/tiles/mountains.png"     # mountains
        ]


class Tile(arcade.Sprite):
    """
    Represents a single square map tile. Has the ability to hold information about the potential unit occupying it.
    """

    def __init__(self, x, y, size: int, cost: int):
        super().__init__(TILE_TYPES[cost])
        self.width = self.height = size
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


class BorderTile(arcade.SpriteList):
    """ A list containing all border segments to be displayed on a single tile. """
    def __init__(self, tile: Tile, neighbors: list, corners: list):
        """
        :param tile: a tile to draw the border on
        :param neighbors: a 4-element boolean list of [bottom, right, top, left]. For instance, bottom = True means
                        that there should be a border on the bottom side of the tile.
        :param corners: the same as neighbors but [lower right, upper right, upper left, lower left]
        """
        super().__init__()
        self.tile = tile
        for i, neighbor in enumerate(neighbors):
            if neighbor:
                corners[i] = corners[i-1] = False
                element = arcade.Sprite("resources/sprites/border_side.png")
                element.width = tile.width
                element.height = tile.height
                element.center_x = tile.center_x
                element.center_y = tile.center_y
                element.color = tile.owner.color
                element.angle = i * 90
                self.append(element)

        for i, corner in enumerate(corners):
            if corner:
                element = arcade.Sprite("resources/sprites/border_corner.png")
                element.width = tile.width
                element.height = tile.height
                element.center_x = tile.center_x
                element.center_y = tile.center_y
                element.color = tile.owner.color
                element.angle = i * 90
                self.append(element)

