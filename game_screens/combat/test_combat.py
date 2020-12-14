import unittest

from game_screens.game_logic import GameLogic
from game_screens.tiles import Tile

CIV_ONE = "The Great Northern"
CIV_TWO = "Mixtec"


class MyTestCase(unittest.TestCase):
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

    def test_only_fight(self):
        # test only method invoking combat between military units
        self.game_logic.add_unit(2, 2, 'one', 'Poor Infantry', 10)
        self.game_logic.add_unit(2, 3, 'two', 'Archers', 2)
        u1 = self.game_logic.get_tile(2, 2).occupant
        u2 = self.game_logic.get_tile(2, 3).occupant
        winner = u1.attack(u2, seed=10)

        self.assertEqual(winner, u1)
        self.assertEqual(winner.health, 130)
        self.assertLessEqual(u2.health, 0)

    def test_move_and_fight(self):
        # test combat resulting from one unit moving to the place occupied by another
        self.setUp()
        self.game_logic.add_unit(2, 2, 'one', 'Poor Infantry', 10)
        self.game_logic.add_unit(2, 3, 'two', 'Archers', 2)
        loser = self.game_logic.players['two']
        u1 = self.game_logic.get_tile(2, 2).occupant
        u2 = self.game_logic.get_tile(2, 3).occupant

        self.assertIn(u2, loser.units)
        self.game_logic.move_unit(u1, 2, 3, 0)
        self.assertNotIn(u2, loser.units)

    def test_slaughter_helpless_settlers(self):
        # test combat against non military units
        self.setUp()
        self.game_logic.add_unit(2, 2, 'one', 'Poor Infantry', 10)
        self.game_logic.add_unit(2, 3, 'two', 'Settler', 1)
        loser = self.game_logic.players['two']

        u1 = self.game_logic.get_tile(2, 2).occupant
        u2 = self.game_logic.get_tile(2, 3).occupant

        self.assertIn(u2, loser.units)
        self.game_logic.move_unit(u1, 2, 3, 0)
        self.assertNotIn(u2, loser.units)


if __name__ == '__main__':
    unittest.main()
