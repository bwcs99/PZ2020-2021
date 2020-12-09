import unittest
import os

from game_screens.game_logic import GameLogic
from game_screens.tiles import Tile

from movement_tests import CIV_ONE, CIV_TWO


class MovementTests(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("..")  # for the resources to get loaded properly
        self.tiles = []
        # these have to be added in the order of bottom to top, left to right in order for get_tile(x, y) to work
        # so (0, 0), (1, 0), .... (COLUMNS_NUMBER-1, 0), (0, 1), (1, 1), ...
        # this is a linear map with, from left to right, a column of water, plains, hills, plains, mountains
        for y in range(5):
            self.tiles.append(Tile(0, y, 1, 0))
            self.tiles.append(Tile(1, y, 1, 1))
            self.tiles.append(Tile(2, y, 1, 2))
            self.tiles.append(Tile(3, y, 1, 1))
            self.tiles.append(Tile(4, y, 1, 3))
        self.game_logic = GameLogic(self.tiles, 5, 5, players=[("one", CIV_ONE, "gray"), ("two", CIV_TWO, "red")],
                                    my_nick="one")
        self.game_logic.add_unit(2, 2, "one", settler=True)
        self.settler = self.game_logic.get_tile(2, 2).occupant

    def test_city_building(self):
        player = self.settler.owner
        self.game_logic.build_city(self.settler)  # TODO name
        tile = self.settler.tile
        assert self.settler not in player.units
        assert not tile.occupied()
        city = tile.city
        assert city is not None
        assert city.owner == player

    # TODO border tests
    # TODO Gabi: resource tests





