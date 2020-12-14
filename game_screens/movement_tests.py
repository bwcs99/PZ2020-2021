import unittest
from math import inf

from game_screens.game_logic import GameLogic
from game_screens.tiles import Tile

CIV_ONE = "The Great Northern"
CIV_TWO = "Mixtec"


class MovementTests(unittest.TestCase):
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
        self.game_logic.add_unit(2, 2, "one")
        self.unit = self.game_logic.get_tile(2, 2).occupant
        self.unit.max_movement = 2
        self.unit.reset_movement()

    def test_cost_assignment(self):
        # Tile(x, y, n) should have a cost of n if 0 < n < 3, else inf
        # this means that water and mountains have a cost of inf
        # plains cost 1 and hills cost 2 to move to them
        # let's check if these costs have been correctly assigned
        for y in range(5):
            assert self.game_logic.get_tile(0, y).cost == inf
            assert self.game_logic.get_tile(1, y).cost == 1
            assert self.game_logic.get_tile(2, y).cost == 2
            assert self.game_logic.get_tile(3, y).cost == 1
            assert self.game_logic.get_tile(4, y).cost == inf

    def test_unit_placement(self):
        # a unit has been placed on tile (2, 2) in the setup
        # let's check if it is set as the occupant
        tile = self.game_logic.get_tile(2, 2)
        assert tile.occupant == self.unit
        # and it has the correct tile assigned
        assert self.unit.tile == tile

    def test_movement_range(self):
        # the unit is standing on the central tile
        # the map, labeling each tile with its individual cost, looks like this
        # inf 1 2 1 inf
        # inf 1 2 1 inf
        # inf 1 * 1 inf
        # inf 1 2 1 inf
        # inf 1 2 1 inf
        # we have 2 movement points to spare
        # the unit should be able to move one tile up and down at cost 2 (hill cost)
        # and one tile left and right at cost 1 (plains cost)
        # and one tile diagonally at cost 2 (1 to move left/right + 1 to move up/down because these are plains too)
        # and nowhere else
        expected_range = {(x, y): 2 for x in range(1, 4) for y in range(1, 4)}
        expected_range[2, 2] = 0  # also it's free to stay where it is
        expected_range[1, 2] = expected_range[3, 2] = 1

        unit_range = self.game_logic.get_unit_range(self.unit)
        assert unit_range == expected_range

    def test_simple_move(self):
        # we move one up
        unit_range = self.game_logic.get_unit_range(self.unit)
        self.game_logic.move_unit(self.unit, 2, 3, unit_range[2, 3])
        # the unit should have the cost subtracted from its movement points
        assert self.unit.movement == self.unit.max_movement - unit_range[2, 3]
        # the previous tile should be unoccupied
        assert not self.game_logic.get_tile(2, 2).occupied()
        # and the occupant of the new tile should be out unit
        # and the unit should have this tile assigned
        new_tile = self.game_logic.get_tile(2, 3)
        assert new_tile.occupant == self.unit
        assert self.unit.tile == new_tile

    def test_sequential_move(self):
        # let's assume we move one tile left
        # then we should be able to move again - one tile up or down, and nowhere else
        unit_range = self.game_logic.get_unit_range(self.unit)
        self.game_logic.move_unit(self.unit, 1, 2, unit_range[1, 2])
        new_range = self.game_logic.get_unit_range(self.unit)
        assert len(new_range) == 3  # up, down, or stay in place
        assert self.unit.movement == 1
        # let's move one down now
        assert (1, 1) in new_range
        assert new_range[1, 1] == 1
        self.game_logic.move_unit(self.unit, 1, 1, new_range[1, 1])
        assert self.unit.movement == 0
        new_tile = self.game_logic.get_tile(1, 1)
        assert new_tile.occupant == self.unit
        assert self.unit.tile == new_tile


if __name__ == '__main__':
    unittest.main()
