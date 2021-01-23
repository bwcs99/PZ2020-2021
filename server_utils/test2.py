from .client import Client
from game_screens import *
from game_screens.granary import Granary
from .server import *
import unittest

PORT = 65001
HOST = '127.0.0.1'


class TestNewLogic(unittest.TestCase):
    player1 = Player("a", "elfy", "red")
    player2 = Player("b", "orki", "blue")
    p1_granary = Granary(100, 200, 300, 400)
    p2_granary = Granary(500, 500, 500, 500)

    def test_update_allies_list(self):
        pass

    def test_update_enemies_list(self):
        pass

    def test_handle_buying_process(self):
        pass

    def test_handle_selling_process(self):
        pass


if __name__ == '__main__':
    unittest.main()

