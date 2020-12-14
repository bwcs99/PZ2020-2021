import unittest

from game_screens.game_logic import GameLogic
from game_screens.tiles import Tile

CIV_ONE = "The Great Northern"
CIV_TWO = "Mixtec"


# TODO rewrite those
class MyTestCase(unittest.TestCase):
    def test_combat_1(self):
        # no tile nor owner needed
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
        # self.game_logic.add_unit(2, 2, "one")
        # self.unit = self.game_logic.get_tile(2, 2).occupant
        # self.unit.max_movement = 2
        # self.unit.reset_movement()
        # t = self.game_logic.get_tile(2, 2)
        # p = self.game_logic.players['one']
        # self.unit.complete_building(t, p)
        # t = self.game_logic.get_tile(1, 1)
        # self.unit.move_to(t, 0)
        # print(str(self.unit))

    # def test_combat_2(self):
    #     g1 = Garrison(None, None, 'Poor Infantry', 10)
    #     g2 = Garrison(None, None, 'Cavalry', 10)
    #     winner = g1.attack(g2, seed=10)
    #     self.assertEqual(winner.type, 'Cavalry')


if __name__ == '__main__':
    unittest.main()
