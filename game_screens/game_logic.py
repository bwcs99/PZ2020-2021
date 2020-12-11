import arcade

from .player import Player
from .tiles import Tile, BlinkingTile
from .units import Unit, Settler


class GameLogic:
    def __init__(self, tiles: arcade.SpriteList, row_no: int, col_no: int, players: list, my_nick: str):
        self.TILE_ROWS = row_no
        self.TILE_COLS = col_no
        self.tiles = tiles
        self.units = arcade.SpriteList()
        self.unit_range = arcade.SpriteList()
        self.move_costs = None
        self.cities = arcade.SpriteList()
        self.players = {nick: Player(nick, civ, col) for nick, civ, col in players}
        self.me = self.players[my_nick]
        self.disconnected_players = []

    def update(self):
        self.unit_range.update()

    def draw(self):
        self.tiles.draw()
        self.unit_range.draw()
        while self.disconnected_players:
            player = self.disconnected_players.pop(0)
            self.players.pop(player)
        for player in self.players.values():
            player.cities.draw()
            player.units.draw()

    def end_turn(self):
        """ Gives units their movement points back, and possibly does other cleanup stuff when a player's turn ends."""
        for unit in self.me.units:
            unit.reset_movement()
        self.hide_unit_range()
        self.me.collect_from_cities()  # maybe this should be here?

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

    def add_unit(self, x: int, y: int, owner: str, settler: bool = False):
        """
        Adds a new unit to the map.

        :param x: the x (column) coord of the tile to place the unit on
        :param y: the y (row) coord of the tile to place the unit on
        :param owner: the nickname of the player owning the unit
        :param settler: whether the unit is a settler
        """
        tile = self.get_tile(x, y)
        owner = self.players[owner]
        if settler:
            unit = Settler(tile, owner)
        else:
            unit = Unit(tile, owner)
        tile.occupant = unit
        owner.units.append(unit)

    def can_unit_move(self, unit: Unit, x: int, y: int) -> int or None:
        """
        Determines whether a unit is able to move to the specified tile.

        :param unit: a unit to be moved
        :param x: the x (column) coord of the tile to move the unit to
        :param y: the y (row) coord of the tile to move the unit to
        :returns: the cost of the move if it's possible, else None
        """
        if not self.move_costs:
            return None
        if unit.owner == self.me and (x, y) in self.move_costs and not self.get_tile(x, y).occupied():
            return self.move_costs[x, y]
        else:
            return None

    def is_unit_mine(self, unit: Unit) -> bool:
        """ Allows to check if the specified unit belongs to the player. """
        return unit.owner == self.me

    def move_unit(self, unit: Unit, x: int, y: int, cost: int):
        """
        Moves a unit to the specified tile and updates its movement range.

        :param unit: a unit to be moved
        :param x: the x (column) coord of the tile to move the unit to
        :param y: the y (row) coord of the tile to move the unit to
        :param cost: cost of the move
        """
        tile = self.get_tile(x, y)
        unit.move_to(tile, cost)
        self.hide_unit_range()
        self.display_unit_range(unit)

    def move_opponents_unit(self, x0, y0, x1, y1, cost):
        """
        Moves a unit located on the tile (x0, y0) to the tile (x1, y1) at a specified cost.
        """
        unit = self.get_tile(x0, y0).occupant
        target = self.get_tile(x1, y1)
        unit.move_to(target, cost)

    def build_city(self, unit: Settler):
        """
        Turns a settler unit into a city.
        :param unit: a settler unit establishing the city
        """
        surroundings = []
        x, y = unit.tile.coords
        for x1 in range(x - 1, x + 2):
            for y1 in range(y - 1, y + 2):
                tile = self.get_tile(x1, y1)
                if tile:
                    surroundings.append(tile)

        city = unit.build_city(surroundings)
        unit.owner.units.remove(unit)
        unit.owner.cities.append(city)
        print("Created city area:", city.area)

    def build_opponents_city(self, x: int, y: int):
        """ Turns a settler unit located on tile (x, y) into a city. """
        unit = self.get_tile(x, y).occupant
        self.build_city(unit)

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
