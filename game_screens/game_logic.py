import arcade
from math import inf

TILE_COLORS = [
            (0, 64, 128),    # water
            (112, 169, 0),   # plains
            (16, 128, 64),   # hills
            (128, 128, 128)  # mountains
        ]


class Unit(arcade.sprite.Sprite):
    def __init__(self, color, tile):
        super().__init__(":resources:images/enemies/saw.png")
        self.color = color
        self.tile = tile
        self.width = tile.width
        self.height = tile.height
        self.health = 100
        self.max_movement = self.movement =  5
        self.move_to(tile, 0)

    def get_stats(self):
        return self.health, self.movement

    def move_to(self, tile, cost):
        self.tile.occupant = None
        self.tile = tile
        self.tile.occupant = self
        self.center_x = tile.center_x
        self.center_y = tile.center_y
        self.movement -= cost

    def reset_movement(self):
        self.movement = self.max_movement


class BlinkingTile(arcade.SpriteSolidColor):
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


class Tile(arcade.SpriteSolidColor):
    """
    Represents a single square map tile. Has the ability to hold information about the potential unit occupying it.
    """

    def __init__(self, x, y, size: int, cost: int):
        super().__init__(size, size, TILE_COLORS[cost])
        self.coords = x, y
        self.occupant = None
        self.cost = cost if 0 < cost < 3 else inf

    def occupied(self):
        return bool(self.occupant)


class GameLogic:
    def __init__(self, tiles, row_no, col_no):
        self.TILE_ROWS = row_no
        self.TILE_COLS = col_no
        self.tiles = tiles
        self.units = arcade.SpriteList()
        self.unit_range = arcade.SpriteList()
        self.move_costs = None
        self.cities = arcade.SpriteList()

    def update(self):
        self.unit_range.update()

    def draw(self):
        self.tiles.draw()
        self.unit_range.draw()
        self.cities.draw()
        self.units.draw()

    def end_turn(self):
        for unit in self.units:
            unit.reset_movement()

    def get_tile(self, x, y):
        try:
            return self.tiles[y * self.TILE_COLS + x]
        except IndexError:
            return None

    def display_unit_range(self, unit):
        self.move_costs = self.get_unit_range(unit)
        for x, y in self.move_costs:
            tile = self.get_tile(x, y)
            blink = BlinkingTile(tile)
            self.unit_range.append(blink)

    def hide_unit_range(self):
        self.unit_range = arcade.SpriteList()
        self.move_costs = None

    def add_unit(self, x, y):
        tile = self.get_tile(x, y)
        unit = Unit(arcade.color.PASTEL_RED, tile)  # TODO ownership
        self.units.append(unit)

    def move_unit(self, unit, x, y):
        if False:  # TODO if unit not mine
            return False
        try:
            cost = self.move_costs[x, y]
            tile = self.get_tile(x, y)
            unit.move_to(tile, cost)
            self.hide_unit_range()
            self.display_unit_range(unit)
            return True
        except KeyError:
            return False

    def get_unit_range(self, unit: Unit):
        x, y = unit.tile.coords
        visited = {(x, y): 0}
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            parent_cost = visited[(x, y)]
            for col, row in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
                tile = self.get_tile(col, row)
                if tile:
                    alt_cost = parent_cost + tile.cost
                    if alt_cost <= unit.movement and ((col, row) not in visited or alt_cost < visited[col, row]):
                        queue.append((col, row))
                        visited[col, row] = alt_cost
        return visited
