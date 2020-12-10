import unittest

from .garrison import Garrison


class MyTestCase(unittest.TestCase):
    def test_combat_1(self):
        # no tile nor owner needed
        g1 = Garrison(None, None, 'Archers', 1)
        g2 = Garrison(None, None, 'Poor Infantry', 10)
        winner = g1.attack(g2)
        self.assertEqual(winner.type, 'Poor Infantry')

    def test_combat_2(self):
        g1 = Garrison(None, None, 'Poor Infantry', 10)
        g2 = Garrison(None, None, 'Cavalry', 10)
        winner = g1.attack(g2, seed=10)
        self.assertEqual(winner.type, 'Cavalry')


if __name__ == '__main__':
    unittest.main()
