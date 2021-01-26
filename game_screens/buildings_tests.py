import unittest

from game_screens.game_logic import GameLogic
from game_screens.tiles import Tile

CIV_ONE = "The Great Northern"
CIV_TWO = "Mixtec"


class BuildingsTest(unittest.TestCase):
    def setUp(self) -> None:
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
        self.game_logic.add_unit(2, 2, "one", 'Settler', 1)
        self.settler = self.game_logic.get_tile(2, 2).occupant

        self.area = []
        self.area.append(Tile(0, 1, 1, 0))
        self.area.append(Tile(1, 1, 1, 0))
        self.area.append(Tile(2, 1, 1, 1))
        self.area.append(Tile(2, 2, 1, 2))
        self.area.append(Tile(0, 0, 1, 2))
        self.area.append(Tile(1, 2, 1, 3))

        self.game_logic.build_city(self.settler, "test_name")
        self.tile = self.settler.tile
        self.city = self.tile.city

    def test_mines(self):
        before_goods = self.city.calculate_goods()
        self.city.buildings["Mines"] = True
        after_goods = self.city.calculate_goods()
        self.assertEqual(after_goods["stone"], before_goods["stone"] + 20)

    def test_free_market(self):
        before_goods = self.city.calculate_goods()
        self.city.buildings["Free Market"] = True
        after_goods = self.city.calculate_goods()
        self.assertEqual(after_goods["gold"], before_goods["gold"] + len(self.city.area) * 3)

    def test_free_market_2(self):
        self.city.area.append(Tile(0, 0, 1, 0))

        before_goods = self.city.calculate_goods()
        self.city.buildings["Free Market"] = True
        after_goods = self.city.calculate_goods()
        self.assertEqual(after_goods["gold"], before_goods["gold"] + len(self.city.area) * 3)

    def test_astronomic_tower(self):
        self.game_logic.increase_area(*self.tile.coords)
        self.assertEqual(len(self.city.area), 13)
        self.game_logic.increase_area(*self.tile.coords)
        self.assertEqual(len(self.city.area), 25)

