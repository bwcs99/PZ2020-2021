import unittest

from .battle import go_fighting, SOLDIER_PROPS
from .garrison import Garrison


class MyTestCase(unittest.TestCase):
    def test_combat_1(self):
        # no tile, no owner needed
        g1 = Garrison(None, None, SOLDIER_PROPS[0], 0)
        g2 = Garrison(None, None, SOLDIER_PROPS[1], 10)
        winner = go_fighting(g1, g2)
        self.assertEqual(winner.type, 'KNIGHT')

    def test_combat_2(self):  # KNIGHT vs CAVALRY
        g1 = Garrison(None, None, SOLDIER_PROPS[1], 10)
        g2 = Garrison(None, None, SOLDIER_PROPS[2], 10)
        winner = go_fighting(g1, g2, seed=10)
        self.assertIsNone(winner)  # should end in draw

    def test_combat_3(self):  # million ducks vs Panzerkampfwagen VI Tiger
        g1 = Garrison(None, None, SOLDIER_PROPS[3], 1000000)
        g2 = Garrison(None, None, SOLDIER_PROPS[4], 1)
        winner = go_fighting(g1, g2, seed=10)
        self.assertEqual(winner.type, 'DUCK')


if __name__ == '__main__':
    unittest.main()
