import arcade

from .tiles import Tile, BlinkingTile
from .units import Unit, Settler


class GameLogic:
    def __init__(self, tiles: arcade.SpriteList, row_no: int, col_no: int):
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
        """ Gives units their movement points back, and possibly does other cleanup stuff when a player's turn ends."""
        for unit in self.units:
            unit.reset_movement()
        self.hide_unit_range()

    def get_tile(self, x: int, y: int) -> Tile or None:
        """
        :return: the tile in column x, row y if it exists, else None
        """
        try:
            return self.tiles[y * self.TILE_COLS + x]
        except IndexError:
            return None

    def display_unit_range(self, unit: Unit):
        """ Makes every tile the unit can move to blink. """
        self.move_costs = self.get_unit_range(unit)
        for x, y in self.move_costs:
            tile = self.get_tile(x, y)
            blink = BlinkingTile(tile)
            self.unit_range.append(blink)

    def hide_unit_range(self):
        """ Removes all blinking tiles from the map. """
        self.unit_range = arcade.SpriteList()
        self.move_costs = None

    def add_unit(self, x: int, y: int, settler: bool = False):
        """
        Adds a new unit to the map.

        :param x: the x (column) coord of the tile to place the unit on
        :param y: the y (row) coord of the tile to place the unit on
        :param settler: whether the unit is a settler
        """
        tile = self.get_tile(x, y)
        unit = Settler(arcade.color.PASTEL_RED, tile) if settler else Unit(arcade.color.PASTEL_RED, tile)  # TODO ownership
        self.units.append(unit)

    def can_unit_move(self, unit: Unit, x: int, y: int) -> bool:
        """
        Determines whether a unit is able to move to the specified tile.

        :param unit: a unit to be moved
        :param x: the x (column) coord of the tile to move the unit to
        :param y: the y (row) coord of the tile to move the unit to
        """
        return (x, y) in self.move_costs  # TODO and unit.mine?

    def move_unit(self, unit: Unit, x: int, y: int):
        """
        Moves a unit to the specified tile and updates its movement range.

        :param unit: a unit to be moved
        :param x: the x (column) coord of the tile to move the unit to
        :param y: the y (row) coord of the tile to move the unit to
        """
        cost = self.move_costs[x, y]
        tile = self.get_tile(x, y)
        unit.move_to(tile, cost)
        self.hide_unit_range()
        self.display_unit_range(unit)

    def build_city(self, unit: Settler):
        """
        Turns a settler unit into a city.
        :param unit: a settler unit establishing the city
        """
        city = unit.build_city()
        self.units.remove(unit)
        self.cities.append(city)

    def get_unit_range(self, unit: Unit) -> dict:
        """
        Determines a unit's movement range.

        :param unit: a unit to be moved
        :return: a dictionary with elements of (x,y):cost
        """
        x, y = unit.tile.coords
        visited = {(x, y): 0}
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            parent_cost = visited[(x, y)]
            for col, row in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
                tile = self.get_tile(col, row)
                if tile:  # TODO one unit per tile but i will do that after the battling system
                    alt_cost = parent_cost + tile.cost
                    if alt_cost <= unit.movement and ((col, row) not in visited or alt_cost < visited[col, row]):
                        queue.append((col, row))
                        visited[col, row] = alt_cost
        return visited
